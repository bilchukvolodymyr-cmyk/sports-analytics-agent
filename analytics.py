import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import statistics

class SportsAnalytics:
    """Аналізує дані про матчи та генерує статистику"""
    
    @staticmethod
    def analyze_team(matches: List[Dict]) -> Dict:
        """
        Аналізує дані команди та генерує статистику
        
        Args:
            matches: Список матчів
            
        Returns:
            Словник зі статистикою
        """
        if not matches:
            return {}
        
        df = pd.DataFrame(matches)
        
        # Основна статистика
        total_matches = len(matches)
        wins = len([m for m in matches if m['result'] == 'W'])
        draws = len([m for m in matches if m['result'] == 'D'])
        losses = len([m for m in matches if m['result'] == 'L'])
        
        total_goals_for = sum([m['home_goals'] for m in matches])
        total_goals_against = sum([m['away_goals'] for m in matches])
        
        total_yellow_cards = sum([m['yellow_cards'] for m in matches])
        total_red_cards = sum([m['red_cards'] for m in matches])
        total_corners = sum([m['corners'] for m in matches])
        
        avg_possession = statistics.mean([m['possession'] for m in matches])
        avg_shots_on_target = statistics.mean([m['shots_on_target'] for m in matches])
        
        # Розраховуємо win rate
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        
        # Очки (за Win = 3, Draw = 1, Loss = 0)
        points = wins * 3 + draws * 1
        
        analytics = {
            'team': matches[0]['team'],
            'total_matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_rate': round(win_rate, 2),
            'points': points,
            'goals_for': total_goals_for,
            'goals_against': total_goals_against,
            'goal_difference': total_goals_for - total_goals_against,
            'avg_goals_per_match': round(total_goals_for / total_matches, 2),
            'yellow_cards': total_yellow_cards,
            'red_cards': total_red_cards,
            'corners': total_corners,
            'avg_corners': round(total_corners / total_matches, 2),
            'avg_possession': round(avg_possession, 2),
            'avg_shots_on_target': round(avg_shots_on_target, 2),
            'matches': matches
        }
        
        return analytics
    
    @staticmethod
    def compare_teams(team1_data: Dict, team2_data: Dict) -> Dict:
        """Порівнює двох команд"""
        comparison = {
            'team1': team1_data['team'],
            'team2': team2_data['team'],
            'team1_stats': team1_data,
            'team2_stats': team2_data,
            'comparison': {
                'Матчи': {
                    team1_data['team']: team1_data['total_matches'],
                    team2_data['team']: team2_data['total_matches']
                },
                'Перемоги': {
                    team1_data['team']: team1_data['wins'],
                    team2_data['team']: team2_data['wins']
                },
                'Нічия': {
                    team1_data['team']: team1_data['draws'],
                    team2_data['team']: team2_data['draws']
                },
                'Поразки': {
                    team1_data['team']: team1_data['losses'],
                    team2_data['team']: team2_data['losses']
                },
                'Голи (всього)': {
                    team1_data['team']: team1_data['goals_for'],
                    team2_data['team']: team2_data['goals_for']
                },
                'Голи пропущено': {
                    team1_data['team']: team1_data['goals_against'],
                    team2_data['team']: team2_data['goals_against']
                },
                'Різниця голів': {
                    team1_data['team']: team1_data['goal_difference'],
                    team2_data['team']: team2_data['goal_difference']
                },
                'Жовті картки': {
                    team1_data['team']: team1_data['yellow_cards'],
                    team2_data['team']: team2_data['yellow_cards']
                },
                'Червоні картки': {
                    team1_data['team']: team1_data['red_cards'],
                    team2_data['team']: team2_data['red_cards']
                },
                'Кутові': {
                    team1_data['team']: team1_data['corners'],
                    team2_data['team']: team2_data['corners']
                },
                'Середня володіння м\'ячем (%)': {
                    team1_data['team']: team1_data['avg_possession'],
                    team2_data['team']: team2_data['avg_possession']
                },
                'Середнє ударів у ворота': {
                    team1_data['team']: team1_data['avg_shots_on_target'],
                    team2_data['team']: team2_data['avg_shots_on_target']
                }
            }
        }
        
        return comparison
    
    @staticmethod
    def get_recent_form(matches: List[Dict], last_n: int = 5) -> str:
        """
        Отримує останню форму команди (останні 5 матчів)
        
        Args:
            matches: Список матчів
            last_n: Кількість останніх матчів для аналізу
            
        Returns:
            Строка з результатами (W/D/L)
        """
        recent = matches[:last_n]
        form = ''.join([m['result'] for m in recent])
        return form
