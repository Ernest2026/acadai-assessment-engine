import re

def process_submission_grading(submission):
    total_score = 0
    answers = submission.answers.all()

    for ans in answers:
        question = ans.question
        
        # Simple Keyword Matching/Density Logic
        if question.expected_answer and ans.answer_text:
            # Normalize and extract keywords
            expected_keywords = set(re.findall(r'\w+', question.expected_answer.lower()))
            student_words = set(re.findall(r'\w+', ans.answer_text.lower()))
            
            if expected_keywords:
                matches = expected_keywords.intersection(student_words)
                match_ratio = len(matches) / len(expected_keywords)
                ans.score = float(question.max_score) * match_ratio
            else:
                ans.score = 0.0
        else:
            ans.score = 0.0
        
        ans.save()
        total_score += ans.score

    submission.total_score = total_score
    submission.grading_status = 'graded'
    submission.save()