<script setup lang="ts">
import { type Task } from '../models/task'
import { type TaskList } from '../models/list'
import { ref, onMounted } from 'vue'
import TaskComponent from '@/components/Task.vue'
import { deleteList } from '@/api/calls/list/listAPICalls'
import { getTasksOfList } from '@/api/calls/list/listAPICalls'
import { updateTaskOrder } from '@/api/calls/task/taskAPICalls'
import DeleteConfirmation from './DeleteConfirmation.vue'
import AddTask from './AddTask.vue'
import { vDraggable } from 'vue-draggable-plus'

const props = defineProps<{ taskList: TaskList }>()
const emit = defineEmits(['listDeleted'])
const tasks = ref<Task[]>([])
const openDeleteListTab = ref(false)

onMounted(async () => {
  tasks.value = await getTasksOfList(props.taskList.id)
  // Sort tasks by order
  tasks.value.sort((a, b) => a.order - b.order)
})

const deleteTaskList = async (list_id: string) => {
  const success = await deleteList(list_id)
  if (success) {
    emit('listDeleted', list_id)
    console.log(`List with id ${list_id} deleted successfully.`)
  } else {
    console.log(`Failed to delete list with id ${list_id}.`)
  }
}

const handleCreatedTask = (task: Task) => {
  tasks.value.push(task)
}

const handleDeletedTask = (taskId: string) => {
  tasks.value = tasks.value.filter(task => task.id !== taskId)
}

// Task drag end handler
const onTaskDragEnd = async (evt: any) => {
  const { oldIndex, newIndex } = evt
  if (oldIndex === newIndex) return

  console.log(
    `Task dragged from index ${oldIndex} to ${newIndex} in list ${props.taskList.name}`
  )

  const moved = [...tasks.value]
  const item = moved.splice(oldIndex, 1)[0]
  moved.splice(newIndex, 0, item)

  // reasign the new positition
  moved.forEach((l, i) => { l.order = i })

  tasks.value = moved

  try {
    const updatePromises = tasks.value.map(task => {
      return updateTaskOrder(task.id, task.order)
    })

    await Promise.all(updatePromises)
    console.log('All tasks order updated successfully')
  } catch (error) {
    console.error('Error updating tasks order:', error)
    // If there's an error, refresh the tasks from the server
    tasks.value = await getTasksOfList(props.taskList.id)
    tasks.value.sort((a, b) => a.order - b.order)
  }
}
</script>

<template>
  <DeleteConfirmation
    :openDeleteConfirmationPopUp="openDeleteListTab"
    :ItemType="'list'"
    :ItemId="props.taskList.id"
    @confirm="deleteTaskList(props.taskList.id); openDeleteListTab = false"
    @cancel="openDeleteListTab = false"
  />

  <article>
    <div class="title-delete-wrapper">
      <h4>{{ props.taskList.name }}</h4>
      <span @click="openDeleteListTab = true" class="remove">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M6 7V18C6 19.1046 6.89543 20 8 20H16C17.1046 20 18 19.1046 18 18V7M6 7H5M6 7H8M18 7H19M18 7H16M10 11V16M14 11V16M8 7V5C8 3.89543 8.89543 3 10 3H14C15.1046 3 16 3.89543 16 5V7M8 7H16"
            stroke="#8c8c8c"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </span>
    </div>

    <ul
      v-draggable="tasks" @end="onTaskDragEnd"
    >
      <li v-for="task in tasks" :key="task.id">
        <TaskComponent
          :task="task"
          @task-deleted="handleDeletedTask(task.id)"
        />
      </li>
      <li>
        <AddTask
          :list-id="props.taskList.id"
          @task-added="handleCreatedTask"
        />
      </li>
    </ul>
  </article>
</template>

<style scoped>
article {
  border: rgb(235, 235, 235) 1px solid;
  border-radius: 8px;
  padding: 16px;
  margin: 16px;
  background-color: white;
  min-width: 280px;
  box-shadow: 0px 0px 4px 1px rgb(129 129 129 / 10%);
}

div.title-delete-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

div.title-delete-wrapper h4 {
  font-family: var(--ff-base);
  color: var(--clr-primary-2);
  margin: 0;
  text-align: center;
}

svg {
  width: 20px;
  cursor: pointer;
}

ul {
  list-style: none;
  padding: 0;
  gap: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
