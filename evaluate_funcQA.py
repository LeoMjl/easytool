#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FuncQA评估脚本
用于计算funcQA任务的正确率和错误率

作者: AI Assistant
创建时间: 2024
"""

import json
import argparse
import os
from typing import Dict, List, Tuple


def load_results(file_path: str) -> List[Dict]:
    """
    加载JSONL格式的结果文件
    
    Args:
        file_path (str): 结果文件路径
        
    Returns:
        List[Dict]: 结果数据列表
        
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"结果文件不存在: {file_path}")
    
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                results.append(data)
            except json.JSONDecodeError as e:
                print(f"警告: 第{line_num}行JSON格式错误: {e}")
                continue
    
    return results


def calculate_metrics(results: List[Dict]) -> Dict[str, float]:
    """
    计算评估指标
    
    Args:
        results (List[Dict]): 结果数据列表
        
    Returns:
        Dict[str, float]: 包含各种指标的字典
    """
    total_count = len(results)
    if total_count == 0:
        return {
            'total': 0,
            'correct': 0,
            'incorrect': 0,
            'accuracy': 0.0,
            'error_rate': 0.0
        }
    
    correct_count = 0
    incorrect_count = 0
    
    for result in results:
        check_index = result.get('check_index', 0)
        if check_index == 1:
            correct_count += 1
        elif check_index == -1:
            incorrect_count += 1
        # check_index为0或其他值的情况不计入正确或错误
    
    # 计算正确率和错误率
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0.0
    error_rate = (incorrect_count / total_count) * 100 if total_count > 0 else 0.0
    
    return {
        'total': total_count,
        'correct': correct_count,
        'incorrect': incorrect_count,
        'accuracy': accuracy,
        'error_rate': error_rate
    }


def analyze_detailed_results(results: List[Dict]) -> Dict[str, List[Dict]]:
    """
    分析详细结果，按正确性分类
    
    Args:
        results (List[Dict]): 结果数据列表
        
    Returns:
        Dict[str, List[Dict]]: 按正确性分类的结果
    """
    correct_results = []
    incorrect_results = []
    uncertain_results = []
    
    for result in results:
        check_index = result.get('check_index', 0)
        simplified_result = {
            'ID': result.get('ID', 'N/A'),
            'question': result.get('question', 'N/A')[:100] + '...' if len(result.get('question', '')) > 100 else result.get('question', 'N/A'),
            'check_index': check_index
        }
        
        if check_index == 1:
            correct_results.append(simplified_result)
        elif check_index == -1:
            incorrect_results.append(simplified_result)
        else:
            uncertain_results.append(simplified_result)
    
    return {
        'correct': correct_results,
        'incorrect': incorrect_results,
        'uncertain': uncertain_results
    }


def print_evaluation_report(metrics: Dict[str, float], detailed_results: Dict[str, List[Dict]], show_details: bool = False):
    """
    打印评估报告
    
    Args:
        metrics (Dict[str, float]): 评估指标
        detailed_results (Dict[str, List[Dict]]): 详细结果分析
        show_details (bool): 是否显示详细信息
    """
    print("\n" + "="*60)
    print("                FuncQA 评估报告")
    print("="*60)
    
    # 基本统计信息
    print(f"\n📊 基本统计:")
    print(f"   总题数:     {metrics['total']:>6}")
    print(f"   正确数:     {metrics['correct']:>6}")
    print(f"   错误数:     {metrics['incorrect']:>6}")
    print(f"   未确定:     {len(detailed_results['uncertain']):>6}")
    
    # 性能指标
    print(f"\n📈 性能指标:")
    print(f"   正确率:     {metrics['accuracy']:>6.2f}%")
    print(f"   错误率:     {metrics['error_rate']:>6.2f}%")
    print(f"   未确定率:   {(len(detailed_results['uncertain'])/metrics['total']*100 if metrics['total'] > 0 else 0):>6.2f}%")
    
    # 详细信息
    if show_details:
        print(f"\n📋 详细信息:")
        
        if detailed_results['incorrect']:
            print(f"\n❌ 错误题目 ({len(detailed_results['incorrect'])}题):")
            for i, result in enumerate(detailed_results['incorrect'][:10], 1):  # 只显示前10题
                print(f"   {i:2d}. ID:{result['ID']} - {result['question']}")
            if len(detailed_results['incorrect']) > 10:
                print(f"   ... 还有 {len(detailed_results['incorrect']) - 10} 题")
        
        if detailed_results['uncertain']:
            print(f"\n❓ 未确定题目 ({len(detailed_results['uncertain'])}题):")
            for i, result in enumerate(detailed_results['uncertain'][:5], 1):  # 只显示前5题
                print(f"   {i:2d}. ID:{result['ID']} - {result['question']}")
            if len(detailed_results['uncertain']) > 5:
                print(f"   ... 还有 {len(detailed_results['uncertain']) - 5} 题")
    
    print("\n" + "="*60)


def save_report_to_file(metrics: Dict[str, float], detailed_results: Dict[str, List[Dict]], output_file: str):
    """
    将评估报告保存到文件
    
    Args:
        metrics (Dict[str, float]): 评估指标
        detailed_results (Dict[str, List[Dict]]): 详细结果分析
        output_file (str): 输出文件路径
    """
    report_data = {
        'summary': {
            'total_questions': metrics['total'],
            'correct_answers': metrics['correct'],
            'incorrect_answers': metrics['incorrect'],
            'uncertain_answers': len(detailed_results['uncertain']),
            'accuracy_percentage': round(metrics['accuracy'], 2),
            'error_rate_percentage': round(metrics['error_rate'], 2),
            'uncertain_rate_percentage': round(len(detailed_results['uncertain'])/metrics['total']*100 if metrics['total'] > 0 else 0, 2)
        },
        'detailed_results': detailed_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 详细报告已保存到: {output_file}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(
        description='FuncQA评估脚本 - 计算正确率和错误率',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python evaluate_funcQA.py FuncQA_funcqa_mh_deepseek-chat_easytool.jsonl
  python evaluate_funcQA.py results.jsonl --details
  python evaluate_funcQA.py results.jsonl --output report.json
        """
    )
    
    parser.add_argument(
        'input_file',
        help='输入的JSONL结果文件路径'
    )
    
    parser.add_argument(
        '--details', '-d',
        action='store_true',
        help='显示详细的错误和未确定题目信息'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='输出详细报告到JSON文件'
    )
    
    args = parser.parse_args()
    
    try:
        # 加载结果文件
        print(f"📂 正在加载结果文件: {args.input_file}")
        results = load_results(args.input_file)
        print(f"✅ 成功加载 {len(results)} 条记录")
        
        # 计算指标
        print("🔢 正在计算评估指标...")
        metrics = calculate_metrics(results)
        
        # 分析详细结果
        detailed_results = analyze_detailed_results(results)
        
        # 打印报告
        print_evaluation_report(metrics, detailed_results, args.details)
        
        # 保存详细报告
        if args.output:
            save_report_to_file(metrics, detailed_results, args.output)
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())