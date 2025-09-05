# od/views.py
import os, csv, io, json, datetime as dt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import UploadForm
from .models import LogUpload, AnalysisRun, AnomalyEvent

def upload_list(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            up = form.save(commit=False)
            up.original_name = request.FILES['file'].name
            up.uploaded_by = request.user if request.user.is_authenticated else None
            up.save()
            messages.success(request, "업로드 완료. 이제 분석을 실행하세요.")
            return redirect('od_upload_list')
    else:
        form = UploadForm()
    uploads = LogUpload.objects.order_by('-created_at')[:50]
    return render(request, 'od/upload_list.html', {'form': form, 'uploads': uploads})

@require_POST
def analyze_now(request, upload_id):
    upload = get_object_or_404(LogUpload, id=upload_id)
    run = AnalysisRun.objects.create(upload=upload)
    # 간단 CSV 파서 + 룰 기반 체크
    path = upload.file.path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='cp949') as f:
            text = f.read()

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)

    # ✅ 아주 단순한 기본 규칙 예시
    # - 타임스탬프 간격 큰 갭
    # - 음수나 비정상 큰 수치
    # - B535/B660/B750 같은 열의 표준편차 과도
    numeric_cols = [c for c in (rows[0].keys() if rows else []) if any(k in c for k in ['B535','B660','B750','B850','B940'])]
    times = []
    for r in rows:
        # 타임스탬프 컬럼 추정 (예: 'time','timestamp')
        t = r.get('time') or r.get('timestamp') or r.get('TIME') or ''
        if t:
            times.append(t)

    events = []
    # 1) 간격 갭 감지 (초간단): 'HH:MM:SS.xxx' 포맷 가정, 20초 이상 벌어지면 경고
    def parse_time(s):
        for fmt in ('%H:%M:%S.%f','%H:%M:%S'):
            try:
                return dt.datetime.strptime(s, fmt)
            except: pass
        return None
    prev = None
    for i, s in enumerate(times):
        tt = parse_time(s)
        if prev and tt:
            gap = (tt - prev).total_seconds()
            if gap >= 20:
                events.append(dict(kind='gap', severity='med', index=i, message=f'간격 {gap:.1f}s', data={'gap_sec': gap}))
        if tt:
            prev = tt

    # 2) 수치 이상 (음수/너무 큼, 표준편차 과도)
    import math
    sums = {c:0.0 for c in numeric_cols}
    sums2= {c:0.0 for c in numeric_cols}
    cnt  = {c:0   for c in numeric_cols}
    max_seen = {c: -1e9 for c in numeric_cols}
    min_seen = {c:  1e9 for c in numeric_cols}

    for i, r in enumerate(rows):
        for c in numeric_cols:
            try:
                v = float(r.get(c,'')) if r.get(c,'') not in ('','NA','NaN') else None
            except:
                v = None
            if v is None:
                continue
            if v < 0:
                events.append(dict(kind='negative', severity='high', index=i, message=f'{c} < 0', data={'value': v}))
            if v > 1e7:  # 임계는 예시
                events.append(dict(kind='huge', severity='high', index=i, message=f'{c} 값 과대', data={'value': v}))
            sums[c]+=v; sums2[c]+=v*v; cnt[c]+=1
            if v>max_seen[c]: max_seen[c]=v
            if v<min_seen[c]: min_seen[c]=v

    cv_high_cols=[]
    for c in numeric_cols:
        if cnt[c] >= 2:
            mean = sums[c]/cnt[c]
            var  = max(sums2[c]/cnt[c] - mean*mean, 0.0)
            std  = math.sqrt(var)
            cv   = (std/mean)*100 if mean else 0.0
            if cv >= 15:  # CV 15% 이상이면 경고(예시)
                cv_high_cols.append((c, round(cv,1)))
    for c, cv in cv_high_cols:
        events.append(dict(kind='cv_high', severity='med', index=None, message=f'{c} CV={cv}%', data={'cv': cv}))

    # DB 저장
    AnomalyEvent.objects.bulk_create([
        AnomalyEvent(run=run, kind=e['kind'], severity=e['severity'], index=e.get('index'),
                     message=e['message'], data=e.get('data',{})) for e in events
    ])
    run.summary = {
        'rows': len(rows),
        'numeric_cols': numeric_cols,
        'events': len(events),
        'cv_high_cols': cv_high_cols,
        'has_gap': any(e['kind']=='gap' for e in events),
    }
    run.ok = len(events) == 0
    run.finished_at = timezone.now()
    run.save()

    messages.info(request, f'분석 완료: 이벤트 {len(events)}건')
    return redirect('od_run_detail', pk=run.id)

def run_detail(request, pk):
    run = get_object_or_404(AnalysisRun, id=pk)
    events = run.events.order_by('-severity')
    return render(request, 'od/run_detail.html', {'run': run, 'events': events})

