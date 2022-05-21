import heapq
from Node import Node


class Aircraft:
    def __init__(self, dep_node:int, arr_node:int, graph, uam_num:int, nodes:list[Node]):
        # number : 항공기번호
        # time_cruising : 총 운항시간
        # time_delay : 총 지연시간
        # route : 비행 경로
        # graph : 도시 그래프 정보
        # idx_route : 비행 경로에 어디쪽에 위치하는지 나타냄
        # can_go : 현재 움직일 수 있는 지 나타냄
        # nodes : 노드들이 담긴 리스트
        # dist_remain : 바로 다음 노드까지 남은 거리
        # 시작하면서 시작 노드의 대기열에 추가하면서 만들어진다.
        self.number = uam_num
        self.time_cruising = 0
        self.time_delay = 0
        self.route = self.dijkstra(graph, dep_node-1, arr_node-1) # dep_node 와 arr_node는 노드번호 1부터
        self.graph = graph
        self.idx_route = 0 # route[idx_route]: 직전노드, route[idx_route+1]: 다음노드
        self.can_go = False
        self.nodes = nodes
        self.dist_remain = self.cal_next_dist()
        # 만들어지면서 출발 노드의 대기열에 등록
        nodes[self.route[0]].put_in_queue(self)

    @staticmethod
    def dijkstra(graph:list, start:int, end:int) -> list:
        # 최단 경로를 찾아주는 알고리즘
        INF = float('inf')
        queue = []
        heapq.heappush(queue, (0, start, [start]))
        result = [INF]*(len(graph)) # 각 노드의 최단거리를 나타내는 그래프
        while queue:
            distance, node_now, route = heapq.heappop(queue)
            if node_now == end:
                return route
            if result[node_now] <= distance: # 이미 최단거리를 적은 노드면 continue
                continue
            result[node_now] = distance

            for i in range(len(graph[node_now])):
                next_node = graph[node_now][i][0]
                next_distance = distance + graph[node_now][i][1]
                heapq.heappush(queue, (next_distance, next_node, route+[next_node]))

    def move(self) -> bool:
        # 움직일 수 있으면 남은 거리에 1 뺀다
        # 움직여서 다음 노드에 도착할 시 남은 거리 정보, 현재 노드, 다음 노드 정보를 업데이트
        # 현재 노드의 대기열에 등록
        # 만약 최종 목적지에 도착하면 return True
        self.time_cruising += 1
        if self.can_go:
            self.dist_remain -= 1
            # 노드에 도착하면
            if self.dist_remain == 0:
                # 진짜 목적지에 도착한 경우
                if self.idx_route == len(self.route) - 2:
                    return True
                self.reach_next()
        else: self.time_delay += 1
        return False

    def cal_next_dist(self) -> int:
        # 다음 노드까지 남은 거리 계산하는 함수
        for n in self.graph[self.route[self.idx_route]]:
            if n[0] == self.route[self.idx_route+1]:
                return n[1]

    def reach_next(self):
        # 노드에 도착한 경우
        # 현재 노드와 다음 노드를 업데이트
        # 도착한 노드의 대기열에 항공기 등록
        # 다음 노드까지의 거리를 업데이트
        self.idx_route += 1
        self.dist_remain = self.cal_next_dist()
        self.nodes[self.route[self.idx_route]].put_in_queue(self)
        self.can_go = False
        return 1
