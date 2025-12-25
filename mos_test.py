import pygame
import os
import json
from pathlib import Path

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
RED = (220, 80, 80)
ORANGE = (255, 165, 0)
DARK_BLUE = (70, 120, 200)
DARK_RED = (180, 50, 50)
DARK_ORANGE = (220, 130, 0)

# Fonts
TITLE_FONT = pygame.font.Font(None, 48)
BUTTON_FONT = pygame.font.Font(None, 36)
LABEL_FONT = pygame.font.Font(None, 24)

# MOS Labels
MOS_LABELS = {
    1: "Bad",
    2: "Poor",
    3: "Fair",
    4: "Good",
    5: "Excellent"
}

# Database file
DB_FILE = "mos_scores.json"
AUDIO_FOLDER = "audios"
ENCOURAGEMENT_IMAGES_FOLDER = "serious_folder"


class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color if hover_color else DARK_BLUE
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        text_surface = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class MOSTest:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("MOS Audio Test")
        self.clock = pygame.time.Clock()
        self.running = True

        # State
        self.state = "menu"  # menu, testing, encouragement
        self.audio_files = self.load_audio_files()
        self.current_audio_index = 0
        self.scores = self.load_scores()
        self.current_audio = None
        self.current_encouragement_message = ""  # Store the current encouragement message
        self.current_encouragement_image = None  # Store the current encouragement image
        self.encouragement_images = self.load_encouragement_images()

        # Check if we should resume
        if self.scores:
            self.current_audio_index = len(self.scores)

    def load_audio_files(self):
        """Load all audio files from the audio folder"""
        audio_extensions = ['.mp3', '.wav', '.ogg']
        audio_files = []

        if os.path.exists(AUDIO_FOLDER):
            for file in sorted(os.listdir(AUDIO_FOLDER)):
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    audio_files.append(os.path.join(AUDIO_FOLDER, file))

        return audio_files

    def load_encouragement_images(self):
        """Load all image files from the encouragement images folder"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp']
        image_files = []

        if os.path.exists(ENCOURAGEMENT_IMAGES_FOLDER):
            for file in os.listdir(ENCOURAGEMENT_IMAGES_FOLDER):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(ENCOURAGEMENT_IMAGES_FOLDER, file))

        return image_files

    def load_scores(self):
        """Load existing scores from database"""
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_scores(self):
        """Save scores to database"""
        with open(DB_FILE, 'w') as f:
            json.dump(self.scores, f, indent=2)

    def reset_scores(self):
        """Reset all scores and start fresh"""
        self.scores = []
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        self.current_audio_index = 0

    def play_current_audio(self):
        """Play the current audio file"""
        if self.current_audio_index < len(self.audio_files):
            audio_file = self.audio_files[self.current_audio_index]
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

    def save_score(self, score):
        """Save the score for current audio"""
        if self.current_audio_index < len(self.audio_files):
            audio_file = self.audio_files[self.current_audio_index]
            self.scores.append({
                "audio_file": audio_file,
                "score": score
            })
            self.save_scores()
            self.current_audio_index += 1

    def undo_last_score(self):
        """Remove the last score and go back to previous audio"""
        if self.scores and self.current_audio_index > 0:
            self.scores.pop()
            self.save_scores()
            self.current_audio_index -= 1
            return True
        return False

    def draw_menu(self):
        """Draw the start menu"""
        self.screen.fill(WHITE)

        # Title
        title = TITLE_FONT.render("MOS Audio Test", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Info text
        if self.scores:
            info_text = f"Progress: {len(self.scores)}/{len(self.audio_files)} audio files rated"
        else:
            info_text = f"Total audio files: {len(self.audio_files)}"

        info = LABEL_FONT.render(info_text, True, BLACK)
        info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(info, info_rect)

        # Buttons
        buttons = []

        if not self.scores:
            # First time - only show start button
            start_btn = Button(WINDOW_WIDTH // 2 - 150, 250, 300, 60, "Start Test")
            buttons.append(("start", start_btn))
        else:
            # Show continue and restart buttons
            continue_btn = Button(WINDOW_WIDTH // 2 - 150, 250, 300, 60, "Continue Test", GREEN)
            restart_btn = Button(WINDOW_WIDTH // 2 - 150, 330, 300, 60, "Restart Test", BLUE)
            buttons.append(("continue", continue_btn))
            buttons.append(("restart", restart_btn))

        return buttons

    def draw_testing(self):
        """Draw the MOS rating interface"""
        self.screen.fill(WHITE)

        # Progress
        progress_text = f"Audio {self.current_audio_index + 1} of {len(self.audio_files)}"
        progress = LABEL_FONT.render(progress_text, True, BLACK)
        progress_rect = progress.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(progress, progress_rect)

        # Audio filename
        if self.current_audio_index < len(self.audio_files):
            filename = os.path.basename(self.audio_files[self.current_audio_index])
            file_text = LABEL_FONT.render(filename, True, DARK_BLUE)
            file_rect = file_text.get_rect(center=(WINDOW_WIDTH // 2, 90))
            self.screen.blit(file_text, file_rect)

        # Instructions
        instruction = TITLE_FONT.render("Rate the Audio Quality", True, BLACK)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(instruction, instruction_rect)

        # MOS rating buttons (1-5)
        buttons = []
        button_width = 120
        button_height = 80
        spacing = 20
        total_width = 5 * button_width + 4 * spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        for i in range(1, 6):
            x = start_x + (i - 1) * (button_width + spacing)
            y = 250
            btn = Button(x, y, button_width, button_height, str(i))
            buttons.append((f"score_{i}", btn))

            # Draw label below button
            label = LABEL_FONT.render(MOS_LABELS[i], True, BLACK)
            label_rect = label.get_rect(center=(x + button_width // 2, y + button_height + 25))
            self.screen.blit(label, label_rect)

        # Play, Repeat, Stop, and Return buttons
        play_btn = Button(WINDOW_WIDTH // 2 - 315, 450, 140, 60, "Play", GREEN)
        repeat_btn = Button(WINDOW_WIDTH // 2 - 160, 450, 140, 60, "Repeat", BLUE)
        stop_btn = Button(WINDOW_WIDTH // 2 - 5, 450, 140, 60, "Stop", RED, DARK_RED)

        # Only show return button if there are previous scores to go back to
        if self.current_audio_index > 0:
            return_btn = Button(WINDOW_WIDTH // 2 + 150, 450, 140, 60, "Return", ORANGE, DARK_ORANGE)
            buttons.append(("return", return_btn))

        buttons.append(("play", play_btn))
        buttons.append(("repeat", repeat_btn))
        buttons.append(("stop", stop_btn))

        return buttons

    def draw_encouragement(self):
        """Draw encouragement window"""
        self.screen.fill(WHITE)

        # Draw the encouragement image at the top-middle if available
        if self.current_encouragement_image:
            try:
                # Load and scale the image
                image = pygame.image.load(self.current_encouragement_image)

                # Scale image to fit nicely (max 300x200 pixels)
                max_width = 300
                max_height = 200
                img_rect = image.get_rect()
                scale_factor = min(max_width / img_rect.width, max_height / img_rect.height)
                new_width = int(img_rect.width * scale_factor)
                new_height = int(img_rect.height * scale_factor)

                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                image_rect = scaled_image.get_rect(center=(WINDOW_WIDTH // 2, 120))
                self.screen.blit(scaled_image, image_rect)

                message_y = 250  # Position message below image
                progress_y = 300
                button_y = 420
            except Exception:
                # If image loading fails, fall back to circle decoration
                pygame.draw.circle(self.screen, GREEN, (WINDOW_WIDTH // 2, 100), 60)
                pygame.draw.circle(self.screen, WHITE, (WINDOW_WIDTH // 2, 100), 50)
                pygame.draw.circle(self.screen, GREEN, (WINDOW_WIDTH // 2, 100), 40)
                message_y = 220
                progress_y = 270
                button_y = 420
        else:
            # No image available, use circle decoration
            pygame.draw.circle(self.screen, GREEN, (WINDOW_WIDTH // 2, 100), 60)
            pygame.draw.circle(self.screen, WHITE, (WINDOW_WIDTH // 2, 100), 50)
            pygame.draw.circle(self.screen, GREEN, (WINDOW_WIDTH // 2, 100), 40)
            message_y = 220
            progress_y = 270
            button_y = 420

        # Draw the ONE encouragement message (already selected when entering this state)
        text = TITLE_FONT.render(self.current_encouragement_message, True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, message_y))
        self.screen.blit(text, text_rect)

        # Draw progress info
        progress_text = f"{len(self.scores)} audio file{'s' if len(self.scores) != 1 else ''} rated!"
        progress = LABEL_FONT.render(progress_text, True, DARK_BLUE)
        progress_rect = progress.get_rect(center=(WINDOW_WIDTH // 2, progress_y))
        self.screen.blit(progress, progress_rect)

        # Continue and Return buttons
        continue_btn = Button(WINDOW_WIDTH // 2 - 220, button_y, 200, 60, "Continue", GREEN)
        return_btn = Button(WINDOW_WIDTH // 2 + 20, button_y, 200, 60, "Return", ORANGE, DARK_ORANGE)

        return [("continue_rating", continue_btn), ("return", return_btn)]

    def draw_completion(self):
        """Draw completion screen"""
        self.screen.fill(WHITE)

        title = TITLE_FONT.render("Test Completed!", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)

        info = LABEL_FONT.render(f"You rated {len(self.scores)} audio files", True, BLACK)
        info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.screen.blit(info, info_rect)

        # Exit button
        exit_btn = Button(WINDOW_WIDTH // 2 - 100, 350, 200, 60, "Exit", BLUE)

        return [("exit", exit_btn)]

    def run(self):
        """Main game loop"""
        while self.running:
            buttons = []

            # Draw current state
            if self.state == "menu":
                buttons = self.draw_menu()
            elif self.state == "testing":
                if self.current_audio_index >= len(self.audio_files):
                    buttons = self.draw_completion()
                else:
                    buttons = self.draw_testing()
            elif self.state == "encouragement":
                buttons = self.draw_encouragement()

            # Draw all buttons
            for _, button in buttons:
                button.draw(self.screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle button clicks
                for action, button in buttons:
                    if button.handle_event(event):
                        self.handle_button_click(action)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_button_click(self, action):
        """Handle button click actions"""
        if action == "start" or action == "continue":
            self.state = "testing"
            # Auto-play audio when starting or continuing
            self.play_current_audio()
        elif action == "restart":
            self.reset_scores()
            self.state = "testing"
            # Auto-play first audio
            self.play_current_audio()
        elif action == "play" or action == "repeat":
            self.play_current_audio()
        elif action == "stop":
            pygame.mixer.music.stop()
        elif action == "return":
            # Go back to previous audio
            if self.undo_last_score():
                pygame.mixer.music.stop()
                self.state = "testing"
                # Auto-play the previous audio
                self.play_current_audio()
        elif action.startswith("score_"):
            score = int(action.split("_")[1])
            self.save_score(score)
            pygame.mixer.music.stop()

            # Check if there are more audio files
            if self.current_audio_index >= len(self.audio_files):
                self.state = "menu"  # Will show completion screen
            else:
                # Pick ONE random encouragement message when entering this state
                import random
                messages = [
                    "Great job!",
                    "Keep going!",
                    "You're doing awesome!",
                    "Excellent work!",
                    "Well done!",
                    "Fantastic!",
                    "Amazing progress!",
                    "You're crushing it!",
                    "Outstanding!",
                    "Keep up the great work!"
                ]
                self.current_encouragement_message = random.choice(messages)

                # Pick ONE random encouragement image
                if self.encouragement_images:
                    self.current_encouragement_image = random.choice(self.encouragement_images)
                else:
                    self.current_encouragement_image = None

                self.state = "encouragement"
        elif action == "continue_rating":
            self.state = "testing"
            # Auto-play next audio when continuing from encouragement screen
            self.play_current_audio()
        elif action == "exit":
            self.running = False


if __name__ == "__main__":
    app = MOSTest()
    app.run()
