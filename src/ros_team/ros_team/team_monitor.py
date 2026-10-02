import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import ChatMessage
from ros_team_msgs.msg import UserPresence
import time

class TeamMonitor(Node):
    def __init__(self):
        super().__init__('team_monitor')


    # SUBSCRIBERS

        self.chat_subscription = self.create_subscription(ChatMessage, '/chat',self.chat_callback, 10)

        self.presence_subscription = self.create_subscription(UserPresence, '/presence',self.presence_callback, 10)

    # USER TRACKING

        self.users = {}

    # ROS NODE TRACKING

        self.known_nodes = set()
        self.graph_initialized = False

    # RECENT EVENTS

        self.events = []

    # CHAT MESSAGES

        self.chat_messages = []

    # TIMERS

        self.graph_timer = self.create_timer(2.0,self.check_ros_nodes)

        self.user_timer = self.create_timer(1.0,self.check_users)

        self.get_logger().info('ROS 2 Team Monitor is Running')

        self.print_dashboard()

    # EVENT SYSTEM

    def add_event(self, event):

        self.events.append(event)

        # keep only the latest 8 events
        if len(self.events) > 8:
            self.events.pop(0)

        self.print_dashboard()

    # CHAT

    def chat_callback(self, msg):

        chat_messages = (
            f"{msg.sender.username}:"
            f"{msg.message}"
        )

        self.chat_messages.append(chat_messages)

        # keep only latest 8 chat messages
        if len(self.chat_messages) > 8:
            self.chat_messages.pop(0)

        self.print_dashboard()


    # PRESENCE 

    def presence_callback(self,msg):

        user_id = msg.user.user_id
        username = msg.user.username

        current_time = time.time()

        # new user
        if user_id not in self.users:

            self.users[user_id] = {

            'username' : username,
            'last_seen' : current_time,
            'online' : True
            }

            self.add_event(f"[USER] {username} has joined")

        else:

            user = self.users[user_id]

            # user came back online
            if not user['online']:

                user['online'] = True

                self.add_event(f"[USER] {username} back online ")

            user['last_seen'] = current_time


    # CHECK OFFLINE USERS

    def check_users(self):

        current_time = time.time()

        for user_id, user in self.users.items():

            if user["online"]:

                time_since_seen = (current_time - user['last_seen'])

                if time_since_seen > 3:

                    user['online'] = False

                    self.add_event(f"[USER] {user['username']} offline")

        self.print_dashboard()


    # ROS GRAPH MONITOR 

    def check_ros_nodes(self):

        node_info = self.get_node_names_and_namespaces()

        current_nodes = set()

        for name, namespace in node_info:

            if namespace == '/':
                full_name = f'/{name}'
            else:
                full_name = (
                    namespace.rstrip('/')
                    + '/'
                    + name
                )

            current_nodes.add(full_name)

        # First scan
        if not self.graph_initialized:

            self.known_nodes = current_nodes
            self.graph_initialized = True

            self.print_dashboard()

            return
        
        # Detect new nodes
        new_nodes = current_nodes - self.known_nodes

        for node in new_nodes:

            self.add_event(f"[ROS] {node} joined")

        # Detect removed nodes

        removed_nodes = self.known_nodes - current_nodes

        for node in removed_nodes:

            self.add_event(f"[ROS] {node} left")

        self.known_nodes = current_nodes

        self.print_dashboard()


    # DASHBOARD

    def print_dashboard(self):

        print("\033[2J\033[H", end="")

        print("========================================")
        print("          ROS 2 TEAM MONITOR")
        print("========================================")

        # USERS

        print("\nUSERS")
        print("----------------------------------------")

        online_users = [
            user
            for user in self.users.values()
            if user['online']
        ]

        if online_users:

            for user in online_users:

                print(f"● {user['username']}    ONLINE")

        else:

            print("No users online")


    # CHAT

        print("\nCHAT")
        print("----------------------------------------")

        if self.chat_messages:

            for message in self.chat_messages:

                print(message)

        else:

            print("No messages yet")

    # ROS NODE

        print("\nROS NODES")
        print("----------------------------------------")

        if self.known_nodes:

            for node in sorted(self.known_nodes):

                print(f"● {node}")

        else:

            print("No ROS nodes detected")


    # EVENTS

        print("\nRECENT EVENTS")
        print("----------------------------------------")

        if self.events:

            for event in self.events:

                print(event)

        else:

            print("No events yet")

        print("\n========================================")


def main(args=None):

    rclpy.init(args=args)
    node = TeamMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()