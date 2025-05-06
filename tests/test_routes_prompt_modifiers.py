from http import HTTPStatus


def test_create_prompt_modifier_valid(client):
    payload = {'name': 'PhraseWithKonjuntiv2', 'prompt': 'Create a phrase in the konjuntiv 2'}

    response = client.post('/prompt-modifiers/', json=payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'PhraseWithKonjuntiv2',
        'prompt': 'Create a phrase in the konjuntiv 2',
        'id': 1,
    }


def test_create_prompt_modifier_repeated_name(client):
    payload = {'name': 'RepeatedName', 'prompt': 'Test prompt modifier'}

    first_response = client.post('/prompt-modifiers/', json=payload)
    assert first_response.status_code == HTTPStatus.CREATED

    second_response = client.post('/prompt-modifiers/', json=payload)
    assert second_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_response.json()['detail'] == (
        'There is already a prompt modifier with the name of RepeatedName'
    )


def test_delete_prompt_modifier_valid(client):
    payload = {'name': 'ToBeDeleted', 'prompt': 'Prompt modifier to be deleted'}

    create_prompt = client.post('/prompt-modifiers/', json=payload)
    assert create_prompt.status_code == HTTPStatus.CREATED

    prompt_modifier_id = create_prompt.json()['id']
    delete_response = client.delete(f'/prompt-modifiers/{prompt_modifier_id}')
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['message'] == 'Prompt modifier deleted'

    get_response = client.get(f'/prompt-modifiers/{prompt_modifier_id}')
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.json()['detail'] == (
        f'Prompt modifier with id {prompt_modifier_id} not found'
    )


def test_delete_prompt_modifier_wrong_id(client):
    # Trying to delete a prompt modifier with an invalid id of 9999
    delete_response = client.delete('/prompt-modifiers/9999')
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_response.json()['detail'] == 'Prompt modifier with id 9999 not found'


def test_get_prompt_modifiers_valid(client):
    payload = {'name': 'PromptModifierTest', 'prompt': 'Prompt modifier in list'}
    client.post('/prompt-modifiers/', json=payload)

    get_response = client.get('/prompt-modifiers/')
    assert get_response.status_code == HTTPStatus.OK

    data = get_response.json()
    assert isinstance(data['prompt_modifiers'], list)
    assert any(prompt['name'] == 'PromptModifierTest' for prompt in data['prompt_modifiers'])


def test_get_prompt_modifiers_limit(client):
    # Testing the response when the 'limit' parameter is applied
    for i in range(25):
        client.post('/prompt-modifiers/', json={'name': f'name{i}', 'prompt': f'prompt{i}'})

    get_response = client.get('/prompt-modifiers/?limit=15')
    assert get_response.status_code == HTTPStatus.OK
    assert len(get_response.json()['prompt_modifiers']) == 15


def test_get_prompt_modifier_by_id_valid(client):
    payload = {'name': 'ToBeRetrieved', 'prompt': 'Prompt modifier to be retrieved'}

    create_prompt = client.post('/prompt-modifiers/', json=payload)
    assert create_prompt.status_code == HTTPStatus.CREATED

    prompt_id = create_prompt.json()['id']
    get_response = client.get(f'/prompt-modifiers/{prompt_id}')
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()['name'] == payload['name']
    assert get_response.json()['prompt'] == payload['prompt']


def test_get_prompt_modifier_by_id_invalid(client):
    # Trying to get a prompt modifier with an invalid id of 9999
    get_response = client.get('/prompt-modifiers/9999')
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.json()['detail'] == 'Prompt modifier with id 9999 not found'


def test_put_prompt_modifier_valid(client):
    payload = {'name': 'ToBeEdited', 'prompt': 'Prompt Modifier to be edited'}

    create_response = client.post('/prompt-modifiers/', json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    prompt_id = create_response.json()['id']
    update_data = {'name': 'EditedName', 'prompt': 'Edited prompt modifier'}
    put_response = client.put(f'/prompt-modifiers/{prompt_id}', json=update_data)
    assert put_response.status_code == HTTPStatus.OK
    assert put_response.json()['message'] == 'The prompt modifier was updated'

    get_response = client.get(f'/prompt-modifiers/{prompt_id}')
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()['name'] == update_data['name']
    assert get_response.json()['prompt'] == update_data['prompt']


def test_put_prompt_modifier_invalid_id(client):
    # Trying to put a prompt modifier with an invalid id of 9999
    update_data = {'name': 'EditedName', 'prompt': 'Edited prompt modifier'}

    put_response = client.put('/prompt-modifiers/9999', json=update_data)
    assert put_response.status_code == HTTPStatus.NOT_FOUND
    assert put_response.json()['detail'] == 'Prompt modifier with id 9999 not found'
