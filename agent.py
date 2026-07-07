from data_fetcher import SportsDataFetcher
from analytics import SportsAnalytics
from visualizer import SportsVisualizer
from typing import List, Dict, Tuple
from datetime import datetime
import os

class SportsAnalyticsAgent:
    """Головний агент для аналізу спортивних подій"""
    
    def __init__(self):
        self.fetcher = SportsDataFetcher()
        self.analytics = SportsAnalytics()
        self.visualizer = SportsVisualizer()
        self.output_dir = "reports"
        
        # Створюємо директорію для звітів
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def analyze_team(self, team_name: str, months: int = 6) -> Dict:
        """
        Аналізує одну команду
        
        Args:
            team_name: Назва команди
            months: Період аналізу в місяцях
            
        Returns:
            Словник з аналітикою
        """
        print(f"\n🔄 Завантажую дані для {team_name}...")
        
        # Отримуємо матчи
        matches = self.fetcher.get_team_matches(team_name, months)
        
        if not matches:
            print(f"❌ Дані для {team_name} не знайдені")
            return {}
        
        print(f"✅ Завантажено {len(matches)} матчів")
        
        # Аналізуємо
        analytics = self.analytics.analyze_team(matches)
        
        return analytics
    
    def compare_teams(self, team1: str, team2: str, months: int = 6) -> Dict:
        """
        Порівнює дві команди
        
        Args:
            team1: Перша команда
            team2: Друга команда
            months: Період аналізу в місяцях
            
        Returns:
            Словник з порівнянням
        """
        print(f"\n⚽ АГЕНТ АНАЛІТИКИ СПОРТИВНИХ ПОДІЙ ⚽")
        print(f"{'='*60}")
        print(f"Порівняння: {team1} vs {team2}")
        print(f"Період: останні {months} місяців")
        print(f"{'='*60}")
        
        # Отримуємо матчи обох команд
        print(f"\n🔄 Завантажую дані...")
        matches1, matches2 = self.fetcher.compare_teams(team1, team2, months)
        
        if not matches1 or not matches2:
            print(f"❌ Помилка при завантаженні даних")
            return {}
        
        print(f"✅ Завантажено {len(matches1)} матчів для {team1}")
        print(f"✅ Завантажено {len(matches2)} матчів для {team2}")
        
        # Аналізуємо обидві команди
        print(f"\n📊 Аналізую команди...")
        team1_analytics = self.analytics.analyze_team(matches1)
        team2_analytics = self.analytics.analyze_team(matches2)
        
        # Порівнюємо
        comparison = self.analytics.compare_teams(team1_analytics, team2_analytics)
        
        return comparison
    
    def generate_report(self, comparison_data: Dict, team1: str, team2: str):
        """Генерує детальний звіт"""
        
        print(f"\n📝 Генерую звіт...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Таблиця порівняння
        comparison_table = self.visualizer.create_comparison_table(comparison_data)
        print(comparison_table)
        
        # Таблиця матчів команди 1
        matches_table1 = self.visualizer.create_matches_table(comparison_data['team1_stats']['matches'])
        print(matches_table1)
        
        # Таблиця матчів команди 2
        matches_table2 = self.visualizer.create_matches_table(comparison_data['team2_stats']['matches'])
        print(matches_table2)
        
        # Статистика команди 1
        stats_summary1 = self.visualizer.create_statistics_summary(comparison_data['team1_stats'])
        print(stats_summary1)
        
        # Статистика команди 2
        stats_summary2 = self.visualizer.create_statistics_summary(comparison_data['team2_stats'])
        print(stats_summary2)
        
        # Створюємо графіки
        try:
            print(f"\n📈 Створюю графіки...")
            
            # Графік порівняння
            chart_file = os.path.join(self.output_dir, f"comparison_{team1}_vs_{team2}_{timestamp}.png")
            self.visualizer.create_comparison_charts(comparison_data, chart_file)
            
            # Графік продуктивності команди 1
            perf_file1 = os.path.join(self.output_dir, f"performance_{team1}_{timestamp}.png")
            self.visualizer.create_performance_chart(comparison_data['team1_stats'], perf_file1)
            
            # Графік продуктивності команди 2
            perf_file2 = os.path.join(self.output_dir, f"performance_{team2}_{timestamp}.png")
            self.visualizer.create_performance_chart(comparison_data['team2_stats'], perf_file2)
            
            print(f"✅ Графіки створені у папці '{self.output_dir}'")
        except Exception as e:
            print(f"⚠️ Помилка при створенні графіків: {e}")
        
        # Текстовий звіт
        report_file = os.path.join(self.output_dir, f"report_{team1}_vs_{team2}_{timestamp}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(comparison_table)
            f.write(matches_table1)
            f.write(matches_table2)
            f.write(stats_summary1)
            f.write(stats_summary2)
        
        print(f"✅ Текстовий звіт збережено: {report_file}")
        
        return {
            'comparison_table': comparison_table,
            'stats_summary1': stats_summary1,
            'stats_summary2': stats_summary2,
            'report_file': report_file
        }
    
    def run(self, team1: str, team2: str, months: int = 6) -> Dict:
        """
        Запускає повний аналіз двох команд
        
        Args:
            team1: Перша команда
            team2: Друга команда
            months: Період аналізу в місяцях
            
        Returns:
            Словник з результатами
        """
        # Отримуємо порівняння
        comparison = self.compare_teams(team1, team2, months)
        
        if not comparison:
            return {}
        
        # Генеруємо звіт
        report = self.generate_report(comparison, team1, team2)
        
        return {
            'comparison': comparison,
            'report': report,
            'status': 'success'
        }
