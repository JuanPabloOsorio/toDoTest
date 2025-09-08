import {type TaskList} from '@/models/list'
import { type Task } from '@/models/task'
import { snakeToCamel } from '@/utils/caseConverter'


export async function createList(taskData: TaskList) {
  try {
    const response = await fetch(`http://localhost:8000/lists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "name": taskData.name,
        "order": taskData.order || 0
      }),
    })
    return await response.json().then(resp => snakeToCamel<TaskList>(resp.data))
  } catch (error) {
    console.error('Error creating a list:', error)
  }
}

export async function getLists() {
  try {
    const response = await fetch(`http://localhost:8000/lists`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
    })
    // Convert snake_case keys to camelCase
    return await response.json().then(resp => snakeToCamel<TaskList[]>(resp.data))
  } catch (error) {
    throw new Error('Error trying to fetch lists: ' + error)
  }
}

export async function updateList(listData: TaskList) {
  try {
    const response = await fetch(`http://localhost:8000/lists/${listData.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "name": listData.name,
        "order": listData.order
      }),
    })
    return await response.json().then(resp => snakeToCamel<TaskList>(resp.data))
  } catch (error) {
    console.error('Error updating the list:', error)
  }
}

export async function updateListOrder(listId: string, order: number) {
  try {
    const response = await fetch(`http://localhost:8000/lists/${listId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "order": order
      }),
    })
    return await response.json().then(resp => snakeToCamel<TaskList>(resp.data))
  } catch (error) {
    console.error('Error updating list order:', error)
  }
}

export async function updateAllListsOrder(lists: TaskList[]) {
  try {
    const updatePromises = lists.map(async list => {
      const response = await fetch(`http://localhost:8000/lists/${list.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order: list.order })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to update list ${list.id}: ${errorData.error || 'Unknown error'}`);
      }
      
      return response.json();
    });
    
    const results = await Promise.all(updatePromises);
    console.log('All lists order updated successfully', results);
    return true;
  } catch (error) {
    console.error('Error updating lists order:', error);
    return false;
  }
}

export async function getTasksOfList(listId: string) {
  try {
    const response = await fetch (`http://localhost:8000/lists/${listId}/tasks`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
    })
    // Convert snake_case keys to camelCase
    return await response.json().then(resp => {
      console.log("Original API response data:", resp.data);
      const convertedData = snakeToCamel<Task[]>(resp.data);
      console.log("Converted data:", convertedData);
      return convertedData;
    })
  } catch (error) {
    throw new Error('Error trying to fetch tasks of a list: ' + error)
  }
}

export async function deleteList(listId: string) {
  try {
    const response = await fetch(`http://localhost:8000/lists/${listId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
    return await response.json().then(resp => resp.successful as boolean)
  } catch (error) {
    console.error('Error deleting the list:', error)
  }
}