import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QFont


class WorkerThread(QThread):
    """백그라운드 작업을 위한 스레드 클래스"""
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, duration=5):
        super().__init__()
        self.duration = duration
        self.is_running = True
    
    def run(self):
        """스레드에서 실행될 작업"""
        for i in range(self.duration):
            if not self.is_running:
                break
            self.progress.emit(f"작업 진행 중... {i+1}/{self.duration}")
            time.sleep(1)
        
        if self.is_running:
            self.progress.emit("작업 완료!")
            self.finished.emit()
    
    def stop(self):
        """스레드 중지"""
        self.is_running = False


class SidebarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("사이드바 앱 - PyQt6")
        self.setGeometry(100, 100, 1000, 600)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃 (수평)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 사이드바 생성
        self.create_sidebar()
        
        # 메인 콘텐츠 영역 생성
        self.create_main_content()
        
        # 레이아웃에 추가
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content)
        
        # 사이드바 초기 상태 설정 (숨김)
        self.sidebar_visible = False
        self.toggle_sidebar()
    
    def create_sidebar(self):
        """사이드바 생성"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
        """)
        
        # 사이드바 레이아웃
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)
        
        # 사이드바 제목
        title_label = QLabel("사이드바")
        title_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        sidebar_layout.addWidget(title_label)
        
        # 사이드바 메뉴 항목들
        menu_items = ["홈", "설정", "도구", "도움말", "정보"]
        for item in menu_items:
            menu_btn = QPushButton(item)
            menu_btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: #ecf0f1;
                    border: none;
                    padding: 12px;
                    text-align: left;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """)
            menu_btn.clicked.connect(lambda checked, text=item: self.menu_clicked(text))
            sidebar_layout.addWidget(menu_btn)
        
        # 사이드바 하단 여백
        sidebar_layout.addStretch()
    
    def create_main_content(self):
        """메인 콘텐츠 영역 생성"""
        self.main_content = QFrame()
        self.main_content.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
            }
        """)
        
        # 메인 콘텐츠 레이아웃
        main_content_layout = QVBoxLayout(self.main_content)
        main_content_layout.setContentsMargins(20, 20, 20, 20)
        main_content_layout.setSpacing(20)
        
        # 상단 컨트롤 영역
        control_layout = QHBoxLayout()
        
        # 사이드바 토글 버튼
        self.toggle_btn = QPushButton("☰ 메뉴")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        control_layout.addWidget(self.toggle_btn)
        
        # 스레드 작업 버튼
        self.thread_btn = QPushButton("스레드 작업 시작")
        self.thread_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.thread_btn.clicked.connect(self.start_thread_work)
        control_layout.addWidget(self.thread_btn)
        
        # 작업 중지 버튼
        self.stop_btn = QPushButton("작업 중지")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_thread_work)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        control_layout.addStretch()
        main_content_layout.addLayout(control_layout)
        
        # 로그 영역
        log_label = QLabel("작업 로그:")
        log_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        main_content_layout.addWidget(log_label)
        
        # 로그 텍스트 에디터
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        self.log_text.setMaximumHeight(200)
        main_content_layout.addWidget(self.log_text)
        
        # 메인 콘텐츠 영역
        content_label = QLabel("메인 콘텐츠 영역")
        content_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                border: 2px solid #bdc3c7;
            }
        """)
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_content_layout.addWidget(content_label)
        
        # 하단 여백
        main_content_layout.addStretch()
    
    def toggle_sidebar(self):
        """사이드바 토글 기능"""
        if self.sidebar_visible:
            # 사이드바 숨기기
            self.sidebar.hide()
            self.toggle_btn.setText("☰ 메뉴")
            self.sidebar_visible = False
            self.log_message("사이드바가 숨겨졌습니다.")
        else:
            # 사이드바 보이기
            self.sidebar.show()
            self.toggle_btn.setText("✕ 닫기")
            self.sidebar_visible = True
            self.log_message("사이드바가 표시되었습니다.")
    
    def start_thread_work(self):
        """스레드 작업 시작"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.log_message("이미 작업이 진행 중입니다.")
            return
        
        self.worker_thread = WorkerThread(duration=10)
        self.worker_thread.progress.connect(self.update_progress)
        self.worker_thread.finished.connect(self.thread_finished)
        
        self.worker_thread.start()
        
        # 버튼 상태 변경
        self.thread_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self.log_message("스레드 작업을 시작했습니다...")
    
    def stop_thread_work(self):
        """스레드 작업 중지"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
            self.log_message("스레드 작업이 중지되었습니다.")
        
        # 버튼 상태 복원
        self.thread_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    
    def update_progress(self, message):
        """진행 상황 업데이트"""
        self.log_message(message)
    
    def thread_finished(self):
        """스레드 작업 완료"""
        self.log_message("스레드 작업이 완료되었습니다.")
        
        # 버튼 상태 복원
        self.thread_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    
    def menu_clicked(self, menu_text):
        """사이드바 메뉴 클릭 처리"""
        self.log_message(f"'{menu_text}' 메뉴를 클릭했습니다.")
    
    def log_message(self, message):
        """로그 메시지 추가"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")


def main():
    app = QApplication(sys.argv)
    
    # 앱 스타일 설정
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
    """)
    
    window = SidebarApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
