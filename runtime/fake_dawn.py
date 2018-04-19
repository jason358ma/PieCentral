"""Emulate an instance of Dawn."""

import socket
import threading
import queue
import time
import runtime_pb2
import ansible_pb2
import notification_pb2
import unittest


class FakeDawn:
    DATA = [0]
    SEND_PORT = 1236
    RECV_PORT = 1235
    TCP_PORT = 1234
    DAWN_HZ = 100
    HOST = '127.0.0.1'

    def __init__(self):
        self.udp_recv_queue = queue.Queue()
        self.udp_send_queue = queue.Queue()
        self.tcp_recv_queue = queue.Queue()
        self.tcp_send_queue = queue.Queue()

    def start(self):
        SENDER_THREAD = threading.Thread(
            target=self.udp_sender, name="fake dawn sender")
        RECV_THREAD = threading.Thread(
            target=self.udp_receiver, name="fake dawn receiver")
        SENDER_THREAD.daemon = True
        RECV_THREAD.daemon = True
        RECV_THREAD.start()
        SENDER_THREAD.start()
        MSGQUEUE = queue.Queue()
        TCP_THREAD = threading.Thread(
            target=self.tcp_relay, name="fake dawn tcp")
        TCP_THREAD.daemon = True
        TCP_THREAD.start()
        print("started threads")
        #add_timestamps(MSGQUEUE)


    @staticmethod
    def dawn_packager(status):
        """Create a sample Dawn message."""
        proto_message = ansible_pb2.DawnData()
        proto_message.student_code_status = status
        test_gamepad = proto_message.gamepads.add()
        test_gamepad.index = 0
        test_gamepad.axes.append(.5)
        test_gamepad.buttons.append(True)
        return proto_message.SerializeToString()

    @staticmethod
    def create_enter_idle():
        return FakeDawn.dawn_packager(ansible_pb2.DawnData.IDLE)

    @staticmethod
    def create_enter_auto():
        return FakeDawn.dawn_packager(ansible_pb2.DawnData.AUTONOMOUS)

    @staticmethod
    def create_enter_teleop():
        return FakeDawn.dawn_packager(ansible_pb2.DawnData.TELEOP)

    @staticmethod
    def create_enter_estop():
        return FakeDawn.dawn_packager(ansible_pb2.DawnData.ESTOP)

    # pylint: disable=unused-argument
    def udp_sender(self):
        """Send a sample dawn message on ``port``."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                next_call = time.time()
                msg = self.udp_send_queue.get()
                sock.sendto(msg, (self.HOST, self.SEND_PORT))
                next_call += 1.0 / FakeDawn.DAWN_HZ
                time.sleep(max(next_call - time.time(), 0))

    # pylint: disable=unused-argument
    def udp_receiver(self):
        """Receive messages on port to receive queue."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.HOST, self.RECV_PORT))
        while True:
            msg, _ = sock.recvfrom(2048)
            runtime_message = runtime_pb2.RuntimeData()
            runtime_message.ParseFromString(msg)
            self.udp_recv_queue.put(msg)

    def add_timestamps(msgqueue):
        """Add timestamp messages to ``msgqueue``."""
        for _ in range(10):
            msg = notification_pb2.Notification()
            msg.header = notification_pb2.Notification.TIMESTAMP_DOWN
            msg.timestamps.append(time.perf_counter())
            msg = msg.SerializeToString()
            msgqueue.put(msg)
        return msgqueue

    def udp_send_message(self, msg):
        self.udp_send_queue.put(msg)

    def udp_receive_message(self):
        return self.udp_recv_queue.get()

    def tcp_send_message(self, msg):
        self.tcp_send_queue.put(msg)

    def tcp_receive_message(self):
        return self.tcp_recv_queue.get()

    def upload(self, filename):
        import shutil
        shutil.copy2(filename, "studentCode.py")

    def tcp_relay(self):
        """Sends and receives messages on ``port``."""
        print('tcp_relay')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.HOST, self.TCP_PORT))
        sock.listen(1)
        conn, _ = sock.accept()
        print('accepted')
        while True:
            if not self.tcp_send_queue.empty():
                conn.send(self.tcp_send_queue.get())
            next_call = time.time()
            next_call += 1.0 / FakeDawn.DAWN_HZ
            receive_msg, _ = conn.recvfrom(2048)
            if receive_msg is None:
                continue
            else:
                parser = notification_pb2.Notification()
                parser.ParseFromString(receive_msg)
                self.tcp_recv_queue.put(parser)
            time.sleep(max(next_call - time.time(), 0))

class DawnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.FAKE_DAWN = FakeDawn()
        cls.FAKE_DAWN.start()

    def setUp(self):
        self.FAKE_DAWN.udp_send_message(FakeDawn.create_enter_idle())

    def tearDown(self):
        self.FAKE_DAWN.udp_send_message(FakeDawn.create_enter_idle())

    def test_estop(self):
        self.FAKE_DAWN.upload("e_stop.py")
        self.FAKE_DAWN.udp_send_message(FakeDawn.create_enter_auto())
        while True:
            msg = self.FAKE_DAWN.tcp_receive_message()
            if msg.header == notification_pb2.Notification.CONSOLE_LOGGING:
                break
        self.FAKE_DAWN.udp_send_message(FakeDawn.create_enter_estop())
        time.sleep(3)
        while True:
            try:
                self.FAKE_DAWN.tcp_recv_queue.get_nowait()
            except queue.Empty:
                break
        time.sleep(1)
        self.assertTrue(self.FAKE_DAWN.tcp_recv_queue.empty(), self.FAKE_DAWN.tcp_recv_queue.get())


# Just Here for testing, should not be run regularly
# if __name__ == "__main__":
#     while True:
#         time.sleep(1)
