import re

def process_submission_grading(submission):
    total_score = 0
    # Use the related_name 'answers' to get all student responses
    answers = submission.answers.all() 

    if not answers.exists():
        submission.grading_status = 'failed'
        submission.save()
        return

    for ans in answers:
        question = ans.question
        
        # Ensure there is an expected answer to compare against 
        if question.expected_answer and ans.answer_text:
            # Basic Keyword Matching
            expected = set(re.findall(r'\w+', question.expected_answer.lower()))
            provided = set(re.findall(r'\w+', ans.answer_text.lower()))
            
            if expected:
                matches = expected.intersection(provided)
                # Calculate ratio: (matches / total keywords) * max_score
                score_ratio = len(matches) / len(expected)
                ans.score = float(question.max_score) * score_ratio
                print("graded ans score is ", ans.score)
            else:
                ans.score = 0
        else:
            ans.score = 0
        
        print("notgraded ans score is ", ans.score)
        ans.save()
        total_score += ans.score

    submission.total_score = total_score
    submission.grading_status = 'graded'
    submission.save()