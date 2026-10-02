import sys
import time
import uuid
import signal
import os

import rclpy
from rclpy.node import Node

from ros_team_msgs.msg import ChatMessage
from ros_team_msgs.msg import UserPresence

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QInputDialog,
    QFrame,
)

from PyQt5.QtCore import Qt, QTimer


class TeamGUI(QMainWindow):

    def __init__(self, username):

        super().__init__()

        # ==================================================
        # USER INFORMATION
        # ==================================================

        self.username = username

        self.user_id = str(
            uuid.uuid4()
        )[:6]

        # ==================================================
        # ROS NODE
        # ==================================================

        self.ros_node = Node(
            f"team_gui_{self.user_id}"
        )

        # ==================================================
        # DATA STORAGE
        # ==================================================

        self.users = {}

        self.known_nodes = set()

        # ==================================================
        # CHAT PUBLISHER
        # ==================================================

        self.chat_publisher = (
            self.ros_node.create_publisher(
                ChatMessage,
                "/chat",
                10
            )
        )

        # ==================================================
        # CHAT SUBSCRIBER
        # ==================================================

        self.chat_subscription = (
            self.ros_node.create_subscription(
                ChatMessage,
                "/chat",
                self.chat_callback,
                10
            )
        )

        # ==================================================
        # PRESENCE PUBLISHER
        # ==================================================

        self.presence_publisher = (
            self.ros_node.create_publisher(
                UserPresence,
                "/presence",
                10
            )
        )

        # ==================================================
        # PRESENCE SUBSCRIBER
        # ==================================================

        self.presence_subscription = (
            self.ros_node.create_subscription(
                UserPresence,
                "/presence",
                self.presence_callback,
                10
            )
        )

        # ==================================================
        # WINDOW
        # ==================================================

        self.setWindowTitle(
            "ROS 2 Team Communication"
        )

        self.resize(
            1200,
            750
        )

        # ==================================================
        # CENTRAL WIDGET
        # ==================================================

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            12,
            8,
            12,
            12
        )

        main_layout.setSpacing(
            8
        )

        # ==================================================
        # HEADER
        # ==================================================

        header_container = QWidget()

        header_layout = QGridLayout(
            header_container
        )

        header_layout.setContentsMargins(
            10,
            5,
            10,
            5
        )

        # LEFT SPACER
        left_spacer = QWidget()

        header_layout.addWidget(
            left_spacer,
            0,
            0
        )

        # TITLE
        header = QLabel(
            "ROS 2 TEAM COMMUNICATION"
        )

        header.setAlignment(
            Qt.AlignCenter
        )

        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        header_layout.addWidget(
            header,
            0,
            1
        )

        # DOMAIN STATUS
        domain_id = os.environ.get(
            "ROS_DOMAIN_ID",
            "0"
        )

        self.status_label = QLabel(
            f"● CONNECTED    ROS DOMAIN: {domain_id}"
        )

        self.status_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        header_layout.addWidget(
            self.status_label,
            0,
            2
        )

        header_layout.setColumnStretch(
            0,
            1
        )

        header_layout.setColumnStretch(
            1,
            1
        )

        header_layout.setColumnStretch(
            2,
            1
        )

        main_layout.addWidget(
            header_container
        )

        # ==================================================
        # USER INFORMATION
        # ==================================================

        user_info = QLabel(
            f"USER: {self.username}    |    ID: {self.user_id}"
        )

        user_info.setAlignment(
            Qt.AlignCenter
        )

        user_info.setStyleSheet("""
            QLabel {
                font-size: 13px;
                padding: 5px;
            }
        """)

        main_layout.addWidget(
            user_info
        )

        # ==================================================
        # MAIN AREA
        # ==================================================

        main_area = QHBoxLayout()

        main_area.setSpacing(
            10
        )

        # ==================================================
        # LEFT PANEL
        # ==================================================

        left_frame = QFrame()

        left_frame.setObjectName(
            "panel"
        )

        left_panel = QVBoxLayout(
            left_frame
        )

        left_panel.setContentsMargins(
            12,
            12,
            12,
            12
        )

        left_panel.setSpacing(
            8
        )

        # TEAM MEMBERS TITLE
        members_title = QLabel(
            "TEAM MEMBERS"
        )

        members_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        left_panel.addWidget(
            members_title
        )

        # USER LIST
        self.user_list = QListWidget()

        left_panel.addWidget(
            self.user_list
        )

        # USER ACTIVITY TITLE
        activity_title = QLabel(
            "USER ACTIVITY"
        )

        activity_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        left_panel.addWidget(
            activity_title
        )

        # USER ACTIVITY
        self.activity_log = QTextEdit()

        self.activity_log.setReadOnly(
            True
        )

        left_panel.addWidget(
            self.activity_log
        )

        # ==================================================
        # CENTER PANEL
        # ==================================================

        center_frame = QFrame()

        center_frame.setObjectName(
            "panel"
        )

        center_panel = QVBoxLayout(
            center_frame
        )

        center_panel.setContentsMargins(
            12,
            12,
            12,
            12
        )

        center_panel.setSpacing(
            8
        )

        # CHAT TITLE
        chat_title = QLabel(
            "TEAM CHAT"
        )

        chat_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        center_panel.addWidget(
            chat_title
        )

        # CHAT DISPLAY
        self.chat_display = QTextEdit()

        self.chat_display.setReadOnly(
            True
        )

        center_panel.addWidget(
            self.chat_display
        )

        # ==================================================
        # MESSAGE INPUT
        # ==================================================

        message_layout = QHBoxLayout()

        message_layout.setSpacing(
            8
        )

        self.message_input = QLineEdit()

        self.message_input.setPlaceholderText(
            "Type a message..."
        )

        self.message_input.returnPressed.connect(
            self.send_message
        )

        message_layout.addWidget(
            self.message_input
        )

        # SEND BUTTON
        send_button = QPushButton(
            "SEND"
        )

        send_button.clicked.connect(
            self.send_message
        )

        message_layout.addWidget(
            send_button
        )

        center_panel.addLayout(
            message_layout
        )

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        right_frame = QFrame()

        right_frame.setObjectName(
            "panel"
        )

        right_panel = QVBoxLayout(
            right_frame
        )

        right_panel.setContentsMargins(
            12,
            12,
            12,
            12
        )

        right_panel.setSpacing(
            8
        )

        # ROS NODES TITLE
        nodes_title = QLabel(
            "ROS NODES"
        )

        nodes_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        right_panel.addWidget(
            nodes_title
        )

        # ROS NODE LIST
        self.node_list = QListWidget()

        right_panel.addWidget(
            self.node_list
        )

        # ROS EVENTS TITLE
        ros_events_title = QLabel(
            "ROS EVENTS"
        )

        ros_events_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
            }
        """)

        right_panel.addWidget(
            ros_events_title
        )

        # ROS EVENTS
        self.ros_events = QTextEdit()

        self.ros_events.setReadOnly(
            True
        )

        right_panel.addWidget(
            self.ros_events
        )

        # ==================================================
        # ADD PANELS
        # ==================================================

        main_area.addWidget(
            left_frame,
            1
        )

        main_area.addWidget(
            center_frame,
            2
        )

        main_area.addWidget(
            right_frame,
            1
        )

        main_layout.addLayout(
            main_area
        )

        # ==================================================
        # ROS PROCESSING TIMER
        # ==================================================

        self.ros_timer = QTimer()

        self.ros_timer.timeout.connect(
            self.process_ros
        )

        self.ros_timer.start(
            50
        )

        # ==================================================
        # PRESENCE TIMER
        # ==================================================

        self.presence_timer = QTimer()

        self.presence_timer.timeout.connect(
            self.publish_presence
        )

        self.presence_timer.start(
            1000
        )

        # ==================================================
        # USER CHECK TIMER
        # ==================================================

        self.user_check_timer = QTimer()

        self.user_check_timer.timeout.connect(
            self.check_users
        )

        self.user_check_timer.start(
            1000
        )

        # ==================================================
        # ROS NODE CHECK TIMER
        # ==================================================

        self.node_check_timer = QTimer()

        self.node_check_timer.timeout.connect(
            self.check_ros_nodes
        )

        self.node_check_timer.start(
            2000
        )

    # ======================================================
    # SEND CHAT MESSAGE
    # ======================================================

    def send_message(self):

        message = (
            self.message_input
            .text()
            .strip()
        )

        if not message:
            return

        msg = ChatMessage()

        msg.sender.username = (
            self.username
        )

        msg.sender.user_id = (
            self.user_id
        )

        msg.message = message

        msg.timestamp = int(
            time.time()
        )

        self.chat_publisher.publish(
            msg
        )

        self.message_input.clear()

    # ======================================================
    # CHAT CALLBACK
    # ======================================================

    def chat_callback(self, msg):

        timestamp = time.strftime(
            "%H:%M:%S",
            time.localtime(
                msg.timestamp
            )
        )

        self.chat_display.append(
            f"<b>[{timestamp}] "
            f"{msg.sender.username}</b> "
            f"<span style='color:#8b949e;'>"
            f"[{msg.sender.user_id}]"
            f"</span><br>"
            f"{msg.message}"
        )

    # ======================================================
    # PUBLISH PRESENCE
    # ======================================================

    def publish_presence(self):

        msg = UserPresence()

        msg.user.username = (
            self.username
        )

        msg.user.user_id = (
            self.user_id
        )

        msg.timestamp = int(
            time.time()
        )

        self.presence_publisher.publish(
            msg
        )

    # ======================================================
    # PRESENCE CALLBACK
    # ======================================================

    def presence_callback(self, msg):

        username = (
            msg.user.username
        )

        user_id = (
            msg.user.user_id
        )

        current_time = time.time()

        if user_id not in self.users:

            self.users[user_id] = {
                "username": username,
                "last_seen": current_time
            }

            timestamp = time.strftime(
                "%H:%M:%S"
            )

            self.activity_log.append(
                f"[{timestamp}] "
                f"User joined: "
                f"{username} "
                f"[{user_id}]"
            )

        else:

            self.users[user_id][
                "last_seen"
            ] = current_time

        self.update_user_list()

    # ======================================================
    # CHECK OFFLINE USERS
    # ======================================================

    def check_users(self):

        current_time = time.time()

        users_to_remove = []

        for user_id, user_data in (
            self.users.items()
        ):

            time_since_last_seen = (
                current_time
                - user_data["last_seen"]
            )

            if time_since_last_seen > 3:

                timestamp = time.strftime(
                    "%H:%M:%S"
                )

                self.activity_log.append(
                    f"[{timestamp}] "
                    f"User offline: "
                    f"{user_data['username']} "
                    f"[{user_id}]"
                )

                users_to_remove.append(
                    user_id
                )

        for user_id in users_to_remove:

            del self.users[
                user_id
            ]

        self.update_user_list()

    # ======================================================
    # UPDATE TEAM MEMBER LIST
    # ======================================================

    def update_user_list(self):

        self.user_list.clear()

        # --------------------------------------------------
        # CURRENT USER
        # --------------------------------------------------

        self.user_list.addItem(
            f"● {self.username} "
            f"[{self.user_id}]  (YOU)"
        )

        # --------------------------------------------------
        # OTHER USERS
        # --------------------------------------------------

        for user_id, user_data in (
            self.users.items()
        ):

            if user_id == self.user_id:
                continue

            self.user_list.addItem(
                f"● {user_data['username']} "
                f"[{user_id}]  ONLINE"
            )

    # ======================================================
    # CHECK ROS NODES
    # ======================================================

    def check_ros_nodes(self):

        current_nodes = (
            self.ros_node
            .get_node_names_and_namespaces()
        )

        current_nodes = set(
            current_nodes
        )

        # --------------------------------------------------
        # FIRST SCAN
        # --------------------------------------------------

        if not self.known_nodes:

            self.known_nodes = (
                current_nodes
            )

            self.update_node_list()

            return

        # --------------------------------------------------
        # NEW NODES
        # --------------------------------------------------

        new_nodes = (
            current_nodes
            - self.known_nodes
        )

        for node in new_nodes:

            node_name = (
                self.format_node_name(
                    node
                )
            )

            timestamp = time.strftime(
                "%H:%M:%S"
            )

            self.ros_events.append(
                f"[{timestamp}] "
                f"NODE JOINED: "
                f"{node_name}"
            )

        # --------------------------------------------------
        # REMOVED NODES
        # --------------------------------------------------

        removed_nodes = (
            self.known_nodes
            - current_nodes
        )

        for node in removed_nodes:

            node_name = (
                self.format_node_name(
                    node
                )
            )

            timestamp = time.strftime(
                "%H:%M:%S"
            )

            self.ros_events.append(
                f"[{timestamp}] "
                f"NODE LEFT: "
                f"{node_name}"
            )

        self.known_nodes = (
            current_nodes
        )

        self.update_node_list()

    # ======================================================
    # UPDATE ROS NODE LIST
    # ======================================================

    def update_node_list(self):

        self.node_list.clear()

        for node in sorted(
            self.known_nodes
        ):

            node_name = (
                self.format_node_name(
                    node
                )
            )

            self.node_list.addItem(
                f"● {node_name}"
            )

    # ======================================================
    # FORMAT ROS NODE NAME
    # ======================================================

    def format_node_name(self, node):

        node_name, namespace = node

        if namespace == "/":

            return f"/{node_name}"

        return (
            f"{namespace}/{node_name}"
        )

    # ======================================================
    # PROCESS ROS
    # ======================================================

    def process_ros(self):

        if rclpy.ok():

            rclpy.spin_once(
                self.ros_node,
                timeout_sec=0
            )

    # ======================================================
    # CLOSE APPLICATION
    # ======================================================

    def closeEvent(self, event):

        self.ros_timer.stop()

        self.presence_timer.stop()

        self.user_check_timer.stop()

        self.node_check_timer.stop()

        self.ros_node.destroy_node()

        if rclpy.ok():

            rclpy.shutdown()

        event.accept()


# ==========================================================
# MAIN
# ==========================================================

def main(args=None):

    rclpy.init(
        args=args
    )

    app = QApplication(
        sys.argv
    )

    # ======================================================
    # DARK ROBOTICS-STYLE THEME
    # ======================================================

    app.setStyleSheet("""
        QMainWindow {
            background-color: #12161c;
        }

        QWidget {
            background-color: #12161c;
            color: #e6edf3;
            font-family: "DejaVu Sans";
        }

        QFrame#panel {
            background-color: #171d25;
            border: 1px solid #303945;
            border-radius: 8px;
        }

        QLabel {
            color: #e6edf3;
        }

        QListWidget,
        QTextEdit,
        QLineEdit {
            background-color: #1b222c;
            color: #e6edf3;
            border: 1px solid #303945;
            border-radius: 6px;
            padding: 6px;
        }

        QListWidget {
            padding: 4px;
        }

        QListWidget::item {
            padding: 7px;
            border-radius: 4px;
        }

        QListWidget::item:selected {
            background-color: #263342;
        }

        QLineEdit {
            padding: 9px;
        }

        QPushButton {
            background-color: #263342;
            color: #e6edf3;
            border: 1px solid #3a4654;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #314052;
        }

        QPushButton:pressed {
            background-color: #1e2833;
        }

        QScrollBar:vertical {
            background: #12161c;
            width: 10px;
            margin: 2px;
        }

        QScrollBar::handle:vertical {
            background: #3a4654;
            border-radius: 5px;
            min-height: 25px;
        }
    """)

    # ======================================================
    # CTRL+C SUPPORT
    # ======================================================

    signal.signal(
        signal.SIGINT,
        lambda sig, frame: app.quit()
    )

    # ======================================================
    # USERNAME INPUT
    # ======================================================

    username, ok = QInputDialog.getText(
        None,
        "ROS 2 Team Communication",
        "Enter your username:"
    )

    if not ok or not username.strip():

        rclpy.shutdown()

        return

    username = username.strip()

    # ======================================================
    # CREATE GUI
    # ======================================================

    window = TeamGUI(
        username
    )

    window.show()

    # ======================================================
    # START APPLICATION
    # ======================================================

    sys.exit(
        app.exec_()
    )


# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":

    main()