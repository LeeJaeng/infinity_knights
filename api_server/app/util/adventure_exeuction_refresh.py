from datetime import datetime, timedelta

"""
    # UTIL : 모험 실행 횟수 새로고침
    # DESCRIPTION
        # 모험 실행 횟수는 매일 초기화
        # 모든 adventure Row를 확인 해서
          updated_date와 현재 날짜가 1일 이상 차이 나면
          execution_count를 0으로 만듬
        # 모험이 시작 되기 전, 모험 리스트 리프레쉬 될 때 사용됨
"""


def adventure_execution_refresh(adventures, request_user):
    time_gap = timedelta(hours=request_user.time_gap)
    curr_date = datetime.utcnow() + time_gap

    refresh = False
    for adventure in adventures:
        last_updated_date = adventure.updated_date + time_gap
        day_diff = (curr_date.date() - last_updated_date.date()).days
        if day_diff >= 1:
            refresh = True
            break

    if refresh:
        for adventure in adventures:
            adventure.execution_count = 0
            adventure.updated_date = datetime.utcnow()
