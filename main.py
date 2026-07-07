#!/usr/bin/env python3
"""
Sports Analytics Agent - Агент для аналізу спортивних подій
"""

import sys
import argparse
from agent import SportsAnalyticsAgent

def main():
    """Головна функція"""
    
    parser = argparse.ArgumentParser(
        description='Агент для аналізу спортивних подій',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  python main.py "Аргентина" "Єгипет"
  python main.py "Англія" "Франція" --months 12
  python main.py "Бразилія" "Уругвай" --months 3
        """
    )
    
    parser.add_argument('team1', help='Перша команда')
    parser.add_argument('team2', help='Друга команда')
    parser.add_argument('--months', type=int, default=6, 
                       help='Період аналізу в місяцях (за замовчуванням: 6)')
    parser.add_argument('--output', help='Папка для збереження звітів')
    
    args = parser.parse_args()
    
    # Створюємо агента
    agent = SportsAnalyticsAgent()
    
    # Запускаємо аналіз
    try:
        result = agent.run(args.team1, args.team2, args.months)
        
        if result['status'] == 'success':
            print("\n✅ Аналіз завершено успішно!")
            print(f"📁 Звіти збережено у папці: {agent.output_dir}")
        else:
            print("\n❌ Помилка при аналізі")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
