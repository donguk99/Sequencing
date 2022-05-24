from Aircraft import *
from Node import *
import collections


def get_graph() -> list:
    f = open('node_info.txt', 'r')
    total_node = int(f.readline())
    node_read = f.readlines()
    graph = [[] for _ in range(total_node)]

    # 그래프에 입력
    for line in node_read:
        start, end, dist = map(int, line.rstrip().split())
        graph[start - 1].append((end - 1, dist))
    f.close()
    result = [total_node] + graph
    return result


def get_schedule() -> collections.deque:
    f = open('dataset3.txt', 'r')
    schedule_temp = [list(map(int, line.rstrip().split())) for line in f]
    schedule = collections.deque(schedule_temp)
    f.close()
    return schedule


def depart():
    # depart
    if schedule:
        next_departure = schedule[0] # schedule은 [이륙시간, 출발, 도착, 항공기번호] 로 되어있다.
    while schedule and t == next_departure[0]:
        # 시간 맞으면 이륙시킴
        if next_departure[1] == next_departure[2]:  # 출발지와 목적지가 같은 경우 그냥 삭제
            schedule.popleft()
            if schedule:
                next_departure = schedule[0]
            continue
        # uam 객체생성하고 떠있는 목록에 추가
        aircraft_cruising.append(Aircraft(next_departure[1], next_departure[2], graph, next_departure[3], nodes))

        schedule.popleft()
        if schedule:
            next_departure = schedule[0]


def update_info():
    # 주변 노드에 자신의 스케쥴과 노드에 에어홀딩 중인 항공기 수 업데이트
    for i in range(total_node):
        for n, _ in graph[i]:
            # 주변 노드 대기중인 항공기 수 업데이트
            nodes[i].aircraft_near_node[n] = len(nodes[n].queue)
            # 주변 노드의 스케쥴 업데이트
            nodes[i].sche_near_node[n] = nodes[n].sche


def put_expect_time(accept_uam):
    i = time_interval
    expect_time = accept_uam.dist_remain
    while i>0:
        if nodes[accept_uam.route[accept_uam.idx_route+1]].sche[expect_time] == 0:
            nodes[accept_uam.route[accept_uam.idx_route+1]].sche[expect_time] = 1
            i -= 1
        expect_time += 1


# ---------------------------------------------------
# 변수
# sq_num : 시퀀싱 번호
# schedule : 스케쥴 표 (시간이 오름차순으로 정렬된 표)
# total_node : 총 노드 개수
# graph : 노드간의 연결과 링크가중치를 표시한 그래프
# nodes : 노드객체들이 저장된 리스트
# aircraft_cruising : 지금 떠있는 UAM 목록
# result : 결과 저장할 리스트 (uam번호, 지연시간) 꼴로 저장된다
# next_departure : 이륙대기중인 UAM
# t : 시간
graph = get_graph()
total_node = graph.pop(0)
# sq_num = int(input())   # 시퀀싱 방식 번호
time_interval = 5



for sq_num in range(1,6):
    nodes = [Node(total_node, i, sq_num, time_interval) for i in range(total_node)]
    aircraft_cruising = []
    will_delete = []
    result = []
    t = 0
    schedule = get_schedule()
    # ------------------------------------------------------
    # 프로그램 시작
    while schedule or aircraft_cruising:
        # move
        for uam in aircraft_cruising:
            if uam.move(): will_delete.append(uam)

        # 도착한 항공기 삭제
        while will_delete:
            uam_will_del = will_delete.pop()
            # 정보 기록
            result.append([uam_will_del.number, uam_will_del.time_delay])
            aircraft_cruising.remove(uam_will_del)
            del uam_will_del

        # depart
        depart()

        if aircraft_cruising:
            # information update
            update_info()

            # sequencing
            for node in nodes:
                accept_uam = node.sequencing()
                if accept_uam:
                    nodes[accept_uam.route[accept_uam.idx_route]].link_uams[accept_uam.route[accept_uam.idx_route+1]] += 1
                    put_expect_time(accept_uam)

            # time update
            for node in nodes:
                node.time_goes()

        t += 1

    # --------------------------------------------------------
    # 기록
    f_name = 'result'+str(sq_num)+'.txt'
    f = open(f_name, 'w')
    f.write("aircraft delay\n")
    result.sort()
    for i in range(len(result)):
        s = str(result[i][0])+' '+str(result[i][1])+'\n'
        f.write(s)
    f.close()