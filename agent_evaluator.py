#!/usr/bin/env python3
"""
Agent Evaluator for Moodle Calendar Sync.

This module provides functionality to evaluate the performance of agents
used in the Moodle Calendar Sync project.
"""

import os
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "agent_evaluator.log"))
    ]
)
logger = logging.getLogger("agent_evaluator")

class AgentEvaluator:
    """
    Evaluator for agent performance in Moodle Calendar Sync.
    
    This class provides methods to evaluate the performance of agents
    used in the Moodle Calendar Sync project, including:
    - Evaluating extraction completeness
    - Evaluating extraction accuracy
    - Evaluating extraction efficiency
    - Generating evaluation reports
    """
    
    def __init__(self, output_dir: str = "evaluations"):
        """
        Initialize the evaluator.
        
        Args:
            output_dir: Directory to store evaluation results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"Initialized evaluator with output directory: {self.output_dir}")
        
        # Initialize evaluation metrics
        self.metrics = {
            "calendar_agent": {},
            "course_agent": {},
            "announcement_agent": {},
            "activity_agent": {},
            "triage_agent": {}
        }
    
    def evaluate_extraction_completeness(self, 
                                        agent_name: str, 
                                        expected_count: int, 
                                        actual_count: int) -> float:
        """
        Evaluate the completeness of data extraction.
        
        Args:
            agent_name: Name of the agent to evaluate
            expected_count: Expected number of items
            actual_count: Actual number of items extracted
            
        Returns:
            float: Completeness score (0-1)
        """
        if expected_count == 0:
            return 1.0
        
        completeness = min(1.0, actual_count / expected_count)
        
        # Store the metric
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {}
        
        self.metrics[agent_name]["completeness"] = completeness
        
        logger.info(f"Evaluated {agent_name} completeness: {completeness:.2f}")
        return completeness
    
    def evaluate_extraction_accuracy(self, 
                                    agent_name: str, 
                                    expected_data: List[Dict[str, Any]], 
                                    actual_data: List[Dict[str, Any]]) -> float:
        """
        Evaluate the accuracy of data extraction.
        
        Args:
            agent_name: Name of the agent to evaluate
            expected_data: Expected data
            actual_data: Actual data extracted
            
        Returns:
            float: Accuracy score (0-1)
        """
        if not expected_data:
            return 1.0
        
        if not actual_data:
            return 0.0
        
        # Simple matching algorithm - can be enhanced for more sophisticated evaluation
        matches = 0
        for expected_item in expected_data:
            for actual_item in actual_data:
                # Check if the item names match
                expected_name = expected_item.get("name", "") or expected_item.get("title", "")
                actual_name = actual_item.get("name", "") or actual_item.get("title", "")
                
                if expected_name.lower() == actual_name.lower():
                    matches += 1
                    break
        
        accuracy = matches / len(expected_data)
        
        # Store the metric
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {}
        
        self.metrics[agent_name]["accuracy"] = accuracy
        
        logger.info(f"Evaluated {agent_name} accuracy: {accuracy:.2f}")
        return accuracy
    
    def evaluate_extraction_efficiency(self, 
                                      agent_name: str, 
                                      execution_time: float, 
                                      item_count: int) -> float:
        """
        Evaluate the efficiency of data extraction.
        
        Args:
            agent_name: Name of the agent to evaluate
            execution_time: Execution time in seconds
            item_count: Number of items extracted
            
        Returns:
            float: Efficiency score (items per second)
        """
        if execution_time <= 0 or item_count <= 0:
            efficiency = 0.0
        else:
            efficiency = item_count / execution_time
        
        # Store the metric
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {}
        
        self.metrics[agent_name]["efficiency"] = efficiency
        
        logger.info(f"Evaluated {agent_name} efficiency: {efficiency:.2f} items/second")
        return efficiency
    
    def evaluate_agent_performance(self, 
                                  agent_name: str, 
                                  expected_data: List[Dict[str, Any]], 
                                  actual_data: List[Dict[str, Any]], 
                                  execution_time: float) -> Dict[str, float]:
        """
        Evaluate the overall performance of an agent.
        
        Args:
            agent_name: Name of the agent to evaluate
            expected_data: Expected data
            actual_data: Actual data extracted
            execution_time: Execution time in seconds
            
        Returns:
            dict: Performance metrics
        """
        logger.info(f"Evaluating performance of {agent_name}")
        
        # Evaluate completeness
        completeness = self.evaluate_extraction_completeness(
            agent_name, 
            len(expected_data), 
            len(actual_data)
        )
        
        # Evaluate accuracy
        accuracy = self.evaluate_extraction_accuracy(
            agent_name, 
            expected_data, 
            actual_data
        )
        
        # Evaluate efficiency
        efficiency = self.evaluate_extraction_efficiency(
            agent_name, 
            execution_time, 
            len(actual_data)
        )
        
        # Calculate overall score
        overall_score = (completeness * 0.4) + (accuracy * 0.4) + (min(1.0, efficiency / 10) * 0.2)
        
        # Store the metrics
        self.metrics[agent_name]["overall_score"] = overall_score
        
        logger.info(f"Overall performance score for {agent_name}: {overall_score:.2f}")
        
        return {
            "completeness": completeness,
            "accuracy": accuracy,
            "efficiency": efficiency,
            "overall_score": overall_score
        }
    
    def generate_evaluation_report(self) -> Dict[str, Any]:
        """
        Generate an evaluation report.
        
        Returns:
            dict: Evaluation report
        """
        logger.info("Generating evaluation report")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics,
            "summary": {}
        }
        
        # Calculate summary metrics
        agent_scores = [
            metrics.get("overall_score", 0.0) 
            for agent_name, metrics in self.metrics.items() 
            if "overall_score" in metrics
        ]
        
        if agent_scores:
            report["summary"]["average_score"] = sum(agent_scores) / len(agent_scores)
            report["summary"]["min_score"] = min(agent_scores)
            report["summary"]["max_score"] = max(agent_scores)
        
        # Save the report
        report_path = self.output_dir / f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Saved evaluation report to {report_path}")
        
        return report
    
    def print_report_summary(self, report: Dict[str, Any]):
        """
        Print a summary of the evaluation report.
        
        Args:
            report: Evaluation report
        """
        print("\n===== Agent Evaluation Report =====")
        print(f"Generated: {report['timestamp']}")
        print("\nAgent Performance Scores:")
        
        for agent_name, metrics in report["metrics"].items():
            if "overall_score" in metrics:
                print(f"  {agent_name}: {metrics['overall_score']:.2f}")
        
        if "summary" in report and "average_score" in report["summary"]:
            print("\nSummary:")
            print(f"  Average Score: {report['summary']['average_score']:.2f}")
            print(f"  Min Score: {report['summary']['min_score']:.2f}")
            print(f"  Max Score: {report['summary']['max_score']:.2f}")
        
        print("\nRecommendations:")
        
        # Generate recommendations based on scores
        for agent_name, metrics in report["metrics"].items():
            if "overall_score" in metrics:
                score = metrics["overall_score"]
                if score < 0.5:
                    print(f"  - {agent_name} needs significant improvement")
                elif score < 0.7:
                    print(f"  - {agent_name} could use some optimization")
                elif score < 0.9:
                    print(f"  - {agent_name} is performing well but has room for improvement")
                else:
                    print(f"  - {agent_name} is performing excellently")
        
        print("====================================")

async def main():
    """Main function to demonstrate the evaluator."""
    try:
        from src.scrapers.simple_moodle_scraper import SimpleMoodleScraper
    except ImportError as e:
        logger.error(f"Failed to import SimpleMoodleScraper: {e}")
        return
    
    # Set up environment variables for mock mode
    os.environ["MOCK_LOGIN"] = "true"
    os.environ["MOCK_CALENDAR_EVENTS"] = "true"
    os.environ["MOODLE_URL"] = "https://moodle.example.com"
    os.environ["MOODLE_USERNAME"] = "test_user"
    os.environ["MOODLE_PASSWORD"] = "test_password"
    os.environ["OPENAI_API_KEY"] = "sk-mock-key"
    
    # Initialize scraper
    scraper = SimpleMoodleScraper(
        base_url="https://moodle.example.com",
        username="test_user",
        password="test_password",
        model="gpt-4o"
    )
    
    # Initialize evaluator
    evaluator = AgentEvaluator()
    
    # Extract course data
    start_time = datetime.now()
    try:
        courses, announcements, activities = await scraper.extract_course_data_with_agents_sdk()
    except Exception as e:
        logger.error(f"Failed to extract course data: {e}")
        return
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    # Define expected data (for demonstration purposes)
    expected_courses = [
        {"name": "Mathematics 101", "id": "MATH101"},
        {"name": "Computer Science 101", "id": "CS101"},
        {"name": "Physics 101", "id": "PHYS101"},
        {"name": "English Literature", "id": "ENG201"},
        {"name": "History of Art", "id": "ART301"}
    ]
    
    expected_announcements = [
        {"title": "Welcome to Mathematics 101", "course": "Mathematics 101"},
        {"title": "Assignment 1 Posted", "course": "Mathematics 101"},
        {"title": "Welcome to Computer Science 101", "course": "Computer Science 101"},
        {"title": "Lab Session Rescheduled", "course": "Computer Science 101"},
        {"title": "Mid-semester Break", "course": ""}
    ]
    
    expected_activities = [
        {"name": "Mathematics Assignment 1", "course": "Mathematics 101"},
        {"name": "Mathematics Quiz 1", "course": "Mathematics 101"},
        {"name": "Computer Science Lab 1", "course": "Computer Science 101"},
        {"name": "Computer Science Quiz 1", "course": "Computer Science 101"},
        {"name": "Physics Lab Report", "course": "Physics 101"},
        {"name": "English Essay", "course": "English Literature"},
        {"name": "Art History Presentation", "course": "History of Art"}
    ]
    
    # Convert Pydantic models to dictionaries if necessary
    actual_courses = []
    if courses:
        for course in courses:
            if hasattr(course, 'model_dump'):
                actual_courses.append(course.model_dump())
            elif hasattr(course, 'dict'):
                actual_courses.append(course.dict())
            else:
                actual_courses.append(course)
    
    actual_announcements = []
    if announcements:
        for announcement in announcements:
            if hasattr(announcement, 'model_dump'):
                actual_announcements.append(announcement.model_dump())
            elif hasattr(announcement, 'dict'):
                actual_announcements.append(announcement.dict())
            else:
                actual_announcements.append(announcement)
    
    actual_activities = []
    if activities:
        for activity in activities:
            if hasattr(activity, 'model_dump'):
                actual_activities.append(activity.model_dump())
            elif hasattr(activity, 'dict'):
                actual_activities.append(activity.dict())
            else:
                actual_activities.append(activity)
    
    # Evaluate agent performance
    evaluator.evaluate_agent_performance(
        "course_agent",
        expected_courses,
        actual_courses,
        execution_time / 3  # Assuming equal time distribution
    )
    
    evaluator.evaluate_agent_performance(
        "announcement_agent",
        expected_announcements,
        actual_announcements,
        execution_time / 3
    )
    
    evaluator.evaluate_agent_performance(
        "activity_agent",
        expected_activities,
        actual_activities,
        execution_time / 3
    )
    
    # Generate and print report
    report = evaluator.generate_evaluation_report()
    evaluator.print_report_summary(report)

if __name__ == "__main__":
    asyncio.run(main())
