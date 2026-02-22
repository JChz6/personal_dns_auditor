def transform_logs(raw_logs: list) -> list:
    transformed = []

    for log in raw_logs:

        client_info = log.get('client:info', {})
        question = log.get('question', {})
        answers = log.get('answer', [])
        rules_raw = log.get('rules', [])

        rules = []
        for rule in rules_raw:
            rules.append(
                {'filter_id': rule.get('filterId'),
                'rule_text' : rule.get('text')}
            )

        record = {
            'time' : log.get('time'),

            'client' : log.get('client'),
            'client_name' : client_info.get('name'),
            'client_disallowed_rule' : client_info.get('disallowed_rule'),
            'client_disallowed' : client_info.get('disallowed'),
            'client_proto' : log.get('client_proto'),

            'question_name' : question.get('name'),
            'question_type' : question.get('type'),
            'question_class' : question.get('class'),

            'status' : log.get('status'),
            'reason' : log.get('reason'),

            'elapsed_ms' : log.get('elapsedMs'),
            'cached' : log.get('cached'),
            'answer_dnssec' : log.get('answer_dnssec'),

            'upstream' : log.get('upstream'),

            'answers' : [
                {
                'type' : a.get('type'),
                'value' : a.get('value'),
                'ttl' : a.get('ttl')
                }
                for a in answers
            ],

            'rules' : rules 
        }

        transformed.append(record)

    return transformed
    
