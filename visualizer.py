import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import io
import base64
from datetime import datetime

# Налаштування стилю
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class SportsVisualizer:
    """Створює графіки та таблиці для аналітики спортивних подій"""
    
    @staticmethod
    def create_comparison_table(comparison_data: Dict) -> str:
        """Створює таблицю порівняння команд"""
        
        team1 = comparison_data['team1']
        team2 = comparison_data['team2']
        comparison = comparison_data['comparison']
        
        # Створюємо таблицю
        table_data = []
        for metric, values in comparison.items():
            table_data.append({
                'Метрика': metric,
                team1: values[team1],
                team2: values[team2]
            })
        
        df_table = pd.DataFrame(table_data)
        
        # Форматуємо та виводимо таблицю
        table_str = "\n" + "="*80 + "\n"
        table_str += f"ПОРІВНЯННЯ: {team1} vs {team2}\n"
        table_str += "="*80 + "\n"
        table_str += df_table.to_string(index=False)
        table_str += "\n" + "="*80 + "\n"
        
        return table_str
    
    @staticmethod
    def create_matches_table(matches: List[Dict]) -> str:
        """Створює таблицю матчів"""
        
        if not matches:
            return "Немає матчів для показу"
        
        df_matches = pd.DataFrame(matches)
        
        # Вибираємо необхідні колонки
        display_cols = ['date', 'opponent', 'home_goals', 'away_goals', 
                       'result', 'yellow_cards', 'corners', 'possession']
        
        if all(col in df_matches.columns for col in display_cols):
            df_display = df_matches[display_cols].copy()
            df_display.columns = ['Дата', 'Опонент', 'Голи', 'Пропущено', 
                                 'Результат', 'Жовті картки', 'Кутові', 'Володіння (%)']
        else:
            df_display = df_matches.head(10)
        
        table_str = "\n" + "="*100 + "\n"
        table_str += f"МАТЧІ КОМАНДИ: {matches[0]['team']} (останні 6 місяців)\n"
        table_str += "="*100 + "\n"
        table_str += df_display.to_string(index=False)
        table_str += "\n" + "="*100 + "\n"
        
        return table_str
    
    @staticmethod
    def create_comparison_charts(comparison_data: Dict, output_file: str = None):
        """Створює графіки для порівняння команд"""
        
        team1 = comparison_data['team1']
        team2 = comparison_data['team2']
        comparison = comparison_data['comparison']
        
        # Вибираємо ключові метрики для графіків
        metrics_to_plot = [
            'Перемоги',
            'Нічия',
            'Поразки',
            'Голи (всього)',
            'Голи пропущено',
            'Жовті картки',
            'Кутові'
        ]
        
        fig, axes = plt.subplots(2, 4, figsize=(16, 10))
        fig.suptitle(f'Порівняння команд: {team1} vs {team2}', fontsize=16, fontweight='bold')
        
        axes = axes.flatten()
        
        for idx, metric in enumerate(metrics_to_plot):
            if metric in comparison:
                values = comparison[metric]
                teams = [team1, team2]
                data = [values[team1], values[team2]]
                
                colors = ['#3498db', '#e74c3c']
                axes[idx].bar(teams, data, color=colors, edgecolor='black', linewidth=1.5)
                axes[idx].set_title(metric, fontweight='bold')
                axes[idx].set_ylabel('Значення')
                
                # Додаємо значення на колонки
                for i, v in enumerate(data):
                    axes[idx].text(i, v + max(data)*0.02, str(v), ha='center', fontweight='bold')
        
        # Приховуємо останній порожній график
        axes[-1].axis('off')
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Графік збережено: {output_file}")
        else:
            plt.show()
        
        return fig
    
    @staticmethod
    def create_performance_chart(team_data: Dict, output_file: str = None):
        """Створює графік продуктивності команди"""
        
        matches = team_data['matches']
        df = pd.DataFrame(matches)
        
        # Сортуємо за датою
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Аналіз продуктивності: {team_data["team"]}', 
                     fontsize=14, fontweight='bold')
        
        # 1. Голи за матчами
        ax1 = axes[0, 0]
        ax1.plot(range(len(df)), df['home_goals'], marker='o', label='Голи забиті', 
                color='#27ae60', linewidth=2, markersize=6)
        ax1.plot(range(len(df)), df['away_goals'], marker='s', label='Голи пропущені', 
                color='#e74c3c', linewidth=2, markersize=6)
        ax1.set_title('Голи за матчами')
        ax1.set_ylabel('Кількість голів')
        ax1.set_xlabel('Матч')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Жовті картки
        ax2 = axes[0, 1]
        ax2.bar(range(len(df)), df['yellow_cards'], color='#f39c12', 
               edgecolor='black', linewidth=1)
        ax2.set_title('Жовті картки за матчами')
        ax2.set_ylabel('Кількість карток')
        ax2.set_xlabel('Матч')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Кутові
        ax3 = axes[1, 0]
        ax3.bar(range(len(df)), df['corners'], color='#3498db', 
               edgecolor='black', linewidth=1)
        ax3.set_title('Кутові за матчами')
        ax3.set_ylabel('Кількість кутових')
        ax3.set_xlabel('Матч')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Володіння м'ячем
        ax4 = axes[1, 1]
        ax4.plot(range(len(df)), df['possession'], marker='D', 
                color='#9b59b6', linewidth=2, markersize=6)
        ax4.axhline(y=50, color='gray', linestyle='--', label='50% (рівномірне)' )
        ax4.set_title('Володіння м\'ячем (%)')
        ax4.set_ylabel('Володіння (%)')
        ax4.set_xlabel('Матч')
        ax4.set_ylim([0, 100])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Графік збережено: {output_file}")
        else:
            plt.show()
        
        return fig
    
    @staticmethod
    def create_statistics_summary(team_data: Dict) -> str:
        """Створює текстове резюме статистики"""
        
        t = team_data
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     СТАТИСТИКА КОМАНДИ: {t['team']:^49} ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 ЗАГАЛЬНА СТАТИСТИКА (останні 6 місяців)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Матчів зіграно:           {t['total_matches']:>3} 
  • Перемоги / Нічия / Поразки: {t['wins']:>2} / {t['draws']:>2} / {t['losses']:>2}
  • Win Rate:                   {t['win_rate']:>5.1f}%
  • Очки:                       {t['points']:>3}

⚽ ГОЛИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Голи забиті:              {t['goals_for']:>3}
  • Голи пропущені:           {t['goals_against']:>3}
  • Різниця голів:            {t['goal_difference']:>+3}
  • Середньо за матч:         {t['avg_goals_per_match']:>5.2f}

🟨 КАРТКИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Жовтих карток:            {t['yellow_cards']:>3}
  • Червоних карток:          {t['red_cards']:>3}

⚽ КУТОВІ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Всього кутових:           {t['corners']:>3}
  • Середньо за матч:         {t['avg_corners']:>5.2f}

🎯 АТАКА
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Середньо ударів у ворота:  {t['avg_shots_on_target']:>5.2f}
  • Володіння м'ячем (%):      {t['avg_possession']:>5.1f}%

╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return summary
