Untitled Beat Game

A rhythm game written in Python using Pygame that automatically generates beat maps from audio files. The project analyzes music, detects beats and onsets, creates a synchronized note chart, and lets the player play the song in a four-lane rhythm game.

Features
Automatic beat map generation from audio files
BPM and onset detection using Librosa
Multiple difficulty levels (Easy, Normal, Hard)
Four-lane rhythm gameplay
Timing-based scoring system
Accuracy calculation
Custom song support (.mp3, .wav, .ogg)
Controls
Key	Lane
A	Left
S	Left Center
W	Right Center
D	Right
Requirements
Python 3.10+
Pygame
Librosa
NumPy
Installation
pip install pygame librosa numpy
How to Run
python PolisosFifow.py
Click Pick a Song
Select an audio file
Press Start Game
The game will automatically generate a beat map if one does not exist
Play using A, S, W, and D
Scoring
Sick – Perfect hit
Good – Great timing
Norm – Acceptable timing
Bad – Late/Early hit
Miss – No hit

The game calculates accuracy based on all notes hit and missed.

Project Structure
PolisosFifow.py      # Main launcher
BeatGameMenu.py      # Main menu
BeatsMaker.py        # Beat map generator
UntitledBeatGame.py  # Gameplay logic
Future Plans
Hold notes
Better visual effects
Song selection improvements
Online leaderboard
Additional game modes
README (Русский)
Untitled Beat Game

Ритм-игра на Python и Pygame, которая автоматически создаёт карты нот на основе музыкальных файлов. Проект анализирует аудио, определяет удары и ритм композиции, создаёт синхронизированную карту и позволяет играть в четырёхполосную ритм-игру.

Возможности
Автоматическая генерация карт нот
Определение BPM и ударов через Librosa
Несколько уровней сложности (Easy, Normal, Hard)
Четыре игровые дорожки
Система оценки по таймингу
Подсчёт точности (Accuracy)
Поддержка собственных песен (.mp3, .wav, .ogg)
Управление
Клавиша	Дорожка
A	Левая
S	Лево-центр
W	Право-центр
D	Правая
Требования
Python 3.10+
Pygame
Librosa
NumPy
Установка
pip install pygame librosa numpy
Запуск
python PolisosFifow.py
Нажмите Pick a Song
Выберите музыкальный файл
Нажмите Start Game
Если карты нет, она будет создана автоматически
Играйте клавишами A, S, W и D
Система оценок
Sick — идеальное попадание
Good — очень хорошее попадание
Norm — нормальное попадание
Bad — плохое попадание
Miss — промах

Точность рассчитывается на основе всех попаданий и промахов.

Структура проекта
PolisosFifow.py      # Запуск проекта
BeatGameMenu.py      # Главное меню
BeatsMaker.py        # Генератор карт
UntitledBeatGame.py  # Игровая логика
Планы на будущее
Длинные ноты (Hold Notes)
Улучшенные визуальные эффекты
Более удобный выбор песен
Онлайн-таблица рекордов
Новые игровые режимы

GitHub short description:

English:
Python rhythm game with automatic beatmap generation from audio files using Librosa and Pygame.

Русский:
Ритм-игра на Python с автоматической генерацией карт нот из музыкальных файлов с помощью Librosa и Pygame.
