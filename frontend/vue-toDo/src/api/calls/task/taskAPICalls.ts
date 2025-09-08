import {type Task} from '@/models/task'
import { snakeToCamel } from '@/utils/caseConverter'


export async function createAPITask(taskData: Task) {
  try {
    const result = await fetch(`http://localhost:8000/task`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
          "title": taskData.title,
          "done": taskData.done,
          "list_id": taskData.listId,
          "description": taskData.description,
          "owner": taskData.owner, 
          "due_date": taskData.dueDate ?? null,
          "attachments": null,
          "checklist": null,
          "order": taskData.order || 0
      }),
    })
    // Convert snake_case keys to camelCase
    return await result.json().then(resp => {
      console.log("Original createAPITask response:", resp.data);
      const convertedData = snakeToCamel<Task>(resp.data);
      console.log("Converted createAPITask data:", convertedData);
      return convertedData;
    })

  } catch (error) {
    console.error('Error al crear la tarea:', error)
  }
}

export async function updateAPITask(taskData: Task) {
  try {
    const result = await fetch(`http://localhost:8000/task/${taskData.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
          "id": taskData.id,
          "title": taskData.title,
          "done": taskData.done,
          "list_id": taskData.listId,
          "description": taskData.description,
          "owner": taskData.owner, 
          "due_date": taskData.dueDate ?? null,
          "attachments": null,
          "checklist": null,
          "order": taskData.order
      }),
    })
    // Return the converted response
    const responseData = await result.json();
    if (responseData.data) {
      console.log("Original updateAPITask response:", responseData.data);
      const convertedData = snakeToCamel<Task>(responseData.data);
      console.log("Converted updateAPITask data:", convertedData);
      return convertedData;
    }
    return null;
  } catch (error) {
    console.error('Error al actualizar la tarea:', error)
  }
}

export async function updateTaskOrder(taskId: string, order: number) {
  try {
    const result = await fetch(`http://localhost:8000/task/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
          "order": order
      }),
    })
    return await result.json().then(resp => {
      if (resp.data) {
        return snakeToCamel<Task>(resp.data);
      }
      return null;
    })
  } catch (error) {
    console.error('Error updating task order:', error)
  }
}


export async function deleteAPITask(task_id: string) {
  try {
    const response = await fetch(`http://localhost:8000/task/${task_id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    })
    return await response.json().then(resp => resp.successful as boolean)
  } catch (error) {
    console.error('Error al eliminar la tarea:', error)
    return false;
  }
}