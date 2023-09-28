
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import threading
import time
import psutil
import gpt4all_chat

class detect_network_traffic(threading.Thread):

    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.trafic = []
        self.running = True
        self.runs = True

    def run(self):
        while self.running:
            self.trafic = check_network_connection(self.trafic)
        self.runs = False

def check_network_connection(network_connections):

    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.status == 'ESTABLISHED'and conn.pid is not None:

            remote_adresses = [
                i.split("'")[1] for i in str(conn).split(",") if "raddr=addr(ip" in i]
            # die strings sind immer gleich aufgebaut
            for i in remote_adresses:
                if not "127.0.0.1" in i:
                    network_connections.append({
                        "remote_adresses": remote_adresses,
                        "pid": conn.pid,
                        "proces_location": psutil.Process(conn.pid).exe(),
                        "proces_name": psutil.Process(conn.pid).name(),

                    })
    return network_connections


def test_models_for_security():
    """_summary_
    """
    # watch network traffic before starting models to have compare data.
    connections_before = check_network_connection([])
    connections_before_str = [ str(i) for i in connections_before]
    connections_before_str = list(set(connections_before_str))


    for model in gpt4all_chat.local_models():
        print("model name:\t",model)
        new_traffic = detect_network_traffic()

        new_traffic.start()
        try:
            chat = gpt4all_chat.Chat(model)
            chat.new_message('write a "Hello world" program in python')
            del chat

        except Exception as e:
            print(e)

        new_traffic.running = False

        while new_traffic.runs:
            time.sleep(1)

        new_traffic_list = new_traffic.trafic
        new_traffic_list = [ str(i) for i in new_traffic_list]
        new_traffic_list = list(set(new_traffic_list))

        for connection in new_traffic_list:
            if not connection in connections_before_str:
                print(connection)
    print("finish security check")

if __name__ == '__main__':
    test_models_for_security()
