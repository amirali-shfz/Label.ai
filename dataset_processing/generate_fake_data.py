import random

def get_fake_submission(num_data_pts, max_user_id, max_class_id):
    submissions = []
    for _ in range(num_data_pts):
        uid = random.randrange(max_user_id)+1
        cid = random.randrange(max_class_id)+1
        class_bool = random.choice(['True', 'False'])
        submissions.append(f'({cid}, {uid}, {class_bool})')
    return submissions

print(', '.join(get_fake_submission(30, 3, 14)))