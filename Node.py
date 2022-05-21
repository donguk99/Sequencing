import collections
import heapq


class Node:
    def __init__(self, total_node:int, node_num:int, sq_num, time_interval):
        # number : 노드 번호
        # queue : 현재 노드 위에 대기중인 항공기 대기열
        # timer : 항공기 간의 간격을 위한 타이머
        # sche : 노드의 스케쥴 (그냥 통과할 수 있을 지 없을 지)
        # sche_near_node : 주변 노드의 스케쥴
        # link_uams : 연결된 링크에 항공기가 얼마나 있는지(노드에서 출발하는 방향)
        # aircraft_near_node : 연결된 노드에 대기중인(에어 홀딩) 항공기 수들
        # sq_num : 시퀀싱 방법
        # time_interval : 하나가 출발하면 얼마 뒤에 출발해야 하는지
        # i : 거쳐간 항공기 수
        self.number = node_num
        self.queue = []
        self.timer = 0
        sche = [0 for _ in range(10000)]
        self.sche = collections.deque(sche)
        self.sche_near_node = [collections.deque([0]) for _ in range(total_node)]
        self.link_uams = [0 for _ in range(total_node)]
        self.aircraft_near_node = [0 for _ in range(total_node)]
        self.sq_num = sq_num
        self.time_interval = time_interval
        self.i = 0

    def sequencing(self):
        # 방법 별 시퀀싱
        self.timer -= 1
        if self.queue and self.timer <= 0:
            if self.sq_num == 1:
                _, _, accept_uam = heapq.heappop(self.queue)
                accept_uam.can_go = True
                self.timer = self.time_interval
                return accept_uam

            elif self.sq_num == 2:
                _, _, accept_uam = heapq.heappop(self.queue)
                accept_uam.can_go = True  # UAM 보내준다
                self.timer = self.time_interval
                return accept_uam

            elif self.sq_num == 3:
                l = []
                idx = 0
                for uam in self.queue:
                    heapq.heappush(l, [self.link_uams[uam.route[uam.idx_route+1]], idx, uam])
                    idx += 1
                _, _, accept_uam = heapq.heappop(l)
                accept_uam.can_go = True  # 보내주기
                self.queue.remove(accept_uam)
                self.timer = self.time_interval
                return accept_uam

            elif self.sq_num == 4:
                l = []
                idx = 0
                for uam in self.queue:
                    heapq.heappush(l, [self.aircraft_near_node[uam.route[uam.idx_route+1]], idx, uam])
                    idx += 1
                _, _, accept_uam = heapq.heappop(l)
                accept_uam.can_go = True  # 보내주기
                self.queue.remove(accept_uam)
                self.timer = self.time_interval
                return accept_uam

            elif self.sq_num == 5:
                l = []
                idx = 0
                for uam in self.queue:
                    wait_time = self.sche_near_node[uam.route[uam.idx_route+1]].index(0, uam.dist_remain) - uam.dist_remain
                    heapq.heappush(l, [wait_time, idx, uam])
                    idx += 1
                _, _, accept_uam = heapq.heappop(l)
                accept_uam.can_go = True
                self.queue.remove(accept_uam)
                self.timer = self.time_interval
                return accept_uam

    def put_in_queue(self, uam):
        # 입력받은 uam을 대기열에 넣는 함수
        if self.sq_num == 1: # 운항시간을 기준
            heapq.heappush(self.queue, [int(self.i), -uam.time_cruising,  uam])
            self.i += 1
        elif self.sq_num == 2: # 지연시간을 기준
            heapq.heappush(self.queue, [-uam.time_delay, int(self.i), uam])
            self.i += 1
        elif self.sq_num == 3 or self.sq_num == 4 or self.sq_num == 5:
            self.queue.append(uam)
            self.i += 1
        else: raise

    def time_goes(self):
        # 시간이 지나면서 변하는 값을 업데이트
        if self.sq_num == 1:
            for i in range(len(self.queue)):
                self.queue[i][1] -= 1
        elif self.sq_num == 2:
            for i in range(len(self.queue)):
                self.queue[i][0] -= 1
        elif self.sq_num == 5:
            self.sche.popleft()