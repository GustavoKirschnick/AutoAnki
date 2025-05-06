from http import HTTPStatus


def test_create_prompt_valid(client):
    payload = {'name': 'CreatePhrase', 'prompt': 'Create a phrase with the following word'}

    response = client.post('/prompts/', json=payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'CreatePhrase',
        'prompt': 'Create a phrase with the following word',
        'id': 1,
    }


def test_create_prompt_repeated_name(client):
    payload = {'name': 'RepeatedName', 'prompt': 'Test prompt'}

    first_response = client.post('/prompts/', json=payload)
    assert first_response.status_code == HTTPStatus.CREATED

    second_response = client.post('/prompts/', json=payload)
    assert second_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_response.json()['detail'] == (
        'There is already a prompt with the name of RepeatedName'
    )


def test_delete_prompt_valid(client):
    payload = {'name': 'ToBeDeleted', 'prompt': 'Prompt to be deleted'}

    create_prompt = client.post('/prompts/', json=payload)
    assert create_prompt.status_code == HTTPStatus.CREATED

    prompt_id = create_prompt.json()['id']
    delete_response = client.delete(f'/prompts/{prompt_id}')
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['message'] == 'Prompt deleted'

    get_response = client.get(f'/prompts/{prompt_id}')
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.json()['detail'] == f'Prompt with id {prompt_id} not found'


def test_delete_prompt_wrong_id(client):
    # Trying to delete a prompt with an invalid id of 9999
    delete_response = client.delete('/prompts/9999')
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_response.json()['detail'] == 'Prompt with id 9999 not found'


def test_get_prompts_valid(client):
    payload = {'name': 'PromptTest', 'prompt': 'Prompt in list'}
    client.post('/prompts/', json=payload)

    get_response = client.get('/prompts/')
    assert get_response.status_code == HTTPStatus.OK

    data = get_response.json()
    assert isinstance(data['prompts'], list)
    assert any(prompt['name'] == 'PromptTest' for prompt in data['prompts'])


def test_get_prompts_limit(client):
    # Testing the response when the 'limit' parameter is applied
    for i in range(25):
        client.post('/prompts/', json={'name': f'name{i}', 'prompt': f'prompt{i}'})

    get_response = client.get('/prompts/?limit=15')
    assert get_response.status_code == HTTPStatus.OK
    assert len(get_response.json()['prompts']) == 15


def test_get_prompt_by_id_valid(client):
    payload = {'name': 'ToBeRetrieved', 'prompt': 'Prompt to be retrieved'}

    create_prompt = client.post('/prompts/', json=payload)
    assert create_prompt.status_code == HTTPStatus.CREATED

    prompt_id = create_prompt.json()['id']
    get_response = client.get(f'/prompts/{prompt_id}')
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()['name'] == payload['name']
    assert get_response.json()['prompt'] == payload['prompt']


def test_get_prompt_by_id_invalid(client):
    # Trying to get a prompt with an invalid id of 9999
    get_response = client.get('/prompts/9999')
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.json()['detail'] == 'Prompt with id 9999 not found'


def test_put_prompt_valid(client):
    payload = {'name': 'ToBeEdited', 'prompt': 'Prompt to be edited'}

    create_response = client.post('/prompts/', json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    prompt_id = create_response.json()['id']
    update_data = {'name': 'EditedName', 'prompt': 'Edited prompt'}
    put_response = client.put(f'/prompts/{prompt_id}', json=update_data)
    assert put_response.status_code == HTTPStatus.OK
    assert put_response.json()['message'] == 'The prompt was updated'

    get_response = client.get(f'/prompts/{prompt_id}')
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()['name'] == update_data['name']
    assert get_response.json()['prompt'] == update_data['prompt']


def test_put_prompt_invalid_id(client):
    # Trying to put a prompt with an invalid id of 9999
    update_data = {'name': 'EditedName', 'prompt': 'Edited prompt'}

    put_response = client.put('/prompts/9999', json=update_data)
    assert put_response.status_code == HTTPStatus.NOT_FOUND
    assert put_response.json()['detail'] == 'Prompt with id 9999 not found'
