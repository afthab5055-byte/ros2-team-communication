import rclpy
from rclpy.node import Node
from ros_team_msgs.msg import ChatMessage
import time
import threading
import uuid

class ChatNode(Node):
    def __init__(self):
        super().__init__('chat_node')
        self.get_logger().info('the node is running')

        self.publisher_ = self.create_publisher(ChatMessage, '/chat', 10)
        self.username = input('Enter your username: ')
        self.user_id = str(uuid.uuid4())[:6]
        self.get_logger().info(f'User ID: {self.user_id}')
        threading.Thread(target=self.input_loop, daemon=True).start()

    def input_loop(self):

        while True:
            message = input('Enter message') # pauses that input thread and wait for the user to type message.
            msg = ChatMessage()

            msg.sender.username = self.username  # everytime the username should be there.
            msg.sender.user_id = self.user_id      # everytime the user_id should be there.

            msg.message = message           # copies the typed text into ROS message.
            msg.timestamp = int(time.time())

            self.publisher_.publish(msg)
        


def main(args=None):
    rclpy.init(args=args)
    node = ChatNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
