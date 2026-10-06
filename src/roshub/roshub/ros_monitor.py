import rclpy
from rclpy.node import Node

class ROSMonitor(Node):
    def __init__(self):
        super().__init__('ros_monitor')
        self.get_logger().info('ROS monitor is running')

        #stores the ros nodes we already know about
        self.known_nodes = set()

        self.timer = self.create_timer(2.0,self.check_nodes)


    def check_nodes(self):

        current_nodes = self.get_node_names_and_namespaces()
        current_nodes = set(current_nodes)

        new_nodes = current_nodes - self.known_nodes

        for node in new_nodes:
            self.get_logger().info(f'ROS node activated {node}')

        removed_nodes = self.known_nodes - current_nodes

        for node in removed_nodes:
            self.get_logger().info(f'ROS node left: {node}')

        self.known_nodes = current_nodes

def main(args=None):
    rclpy.init(args=args)
    node = ROSMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
