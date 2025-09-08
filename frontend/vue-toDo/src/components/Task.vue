<script setup lang="ts">
import { type Task } from '../models/task'
import TaskForm from '@/components/TaskForm.vue'
import { ref, onMounted, type Ref } from 'vue'
import { updateAPITask, deleteAPITask } from '@/api/calls/task/taskAPICalls';
import DeleteConfirmation from './DeleteConfirmation.vue';

const props = defineProps<{ task: Task;}>()
const isOpen = ref(false);
let openDeleteTaskTab = ref(false);


const emit = defineEmits<{
  (e: 'taskDeleted', task_id: string): void;
}>();


let taskMock = ref<Task | null>(null)

const updateTask = async (updatedTask: Task) => {
  console.log("UPDATED TASKS HERE: ", updatedTask);
  try {
    const result = await updateAPITask(updatedTask);
    if (result) {
      // Update the local task with the result from the API
      Object.assign(props.task, result);
      console.log("Task updated successfully:", props.task);
    }
  } catch (error) {
    console.error("Error updating task:", error);
  }
}

const toggleStatus = () => {
  if (props.task) {
    props.task.done = !props.task.done
  }
}

const openForm = () => {
  isOpen.value = true
}

const deleteTaskFromList = async (taskId: string) => {
  const result = await deleteAPITask(taskId);
  openDeleteTaskTab.value = true;
  emit('taskDeleted', taskId);
  
}

</script>

<template>

  <DeleteConfirmation
    :openDeleteConfirmationPopUp="openDeleteTaskTab"
    :ItemType="'task'"
    :ItemId="props.task.id"
    @confirm="deleteTaskFromList(props.task.id); openDeleteTaskTab = false"
    @cancel="openDeleteTaskTab = false"
  />

  <div>
    <article :class="['task-article-' + task.id, 'open']" @click="openForm" :key="task.id">
      <div class="wrapper">
        <svg
          v-if="task.done"
          class="checked-icon"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          @click.stop="toggleStatus"
        >
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path
              d="M9 10L12.2581 12.4436C12.6766 12.7574 13.2662 12.6957 13.6107 12.3021L20 5"
              stroke="#222222"
              stroke-linecap="round"
            ></path>
            <path
              d="M21 12C21 13.8805 20.411 15.7137 19.3156 17.2423C18.2203 18.7709 16.6736 19.9179 14.893 20.5224C13.1123 21.1268 11.187 21.1583 9.38744 20.6125C7.58792 20.0666 6.00459 18.9707 4.85982 17.4789C3.71505 15.987 3.06635 14.174 3.00482 12.2945C2.94329 10.415 3.47203 8.56344 4.51677 6.99987C5.56152 5.4363 7.06979 4.23925 8.82975 3.57685C10.5897 2.91444 12.513 2.81996 14.3294 3.30667"
              stroke="#222222"
              stroke-linecap="round"
            ></path>
          </g>
        </svg>
        <svg
          v-if="!task.done"
          class="unchecked-icon"
          fill="#000000"
          viewBox="0 0 32 32"
          xmlns="http://www.w3.org/2000/svg"
          @click.stop="toggleStatus"
        >
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path
              d="M16,32A16,16,0,1,0,0,16,16,16,0,0,0,16,32ZM16,2A14,14,0,1,1,2,16,14,14,0,0,1,16,2Z"
            ></path>
          </g>
        </svg>
        

        <div class="title-delete-wrapper">
          <p class="task-title">{{ task.title }}</p>
        </div>
        <svg class="edit-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M21.2799 6.40005L11.7399 15.94C10.7899 16.89 7.96987 17.33 7.33987 16.7C6.70987 16.07 7.13987 13.25 8.08987 12.3L17.6399 2.75002C17.8754 2.49308 18.1605 2.28654 18.4781 2.14284C18.7956 1.99914 19.139 1.92124 19.4875 1.9139C19.8359 1.90657 20.1823 1.96991 20.5056 2.10012C20.8289 2.23033 21.1225 2.42473 21.3686 2.67153C21.6147 2.91833 21.8083 3.21243 21.9376 3.53609C22.0669 3.85976 22.1294 4.20626 22.1211 4.55471C22.1128 4.90316 22.0339 5.24635 21.8894 5.5635C21.7448 5.88065 21.5375 6.16524 21.2799 6.40005V6.40005Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M11 4H6C4.93913 4 3.92178 4.42142 3.17163 5.17157C2.42149 5.92172 2 6.93913 2 8V18C2 19.0609 2.42149 20.0783 3.17163 20.8284C3.92178 21.5786 4.93913 22 6 22H17C19.21 22 20 20.2 20 18V13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
        <span @click.stop="openDeleteTaskTab = true" class="remove">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M6 7V18C6 19.1046 6.89543 20 8 20H16C17.1046 20 18 19.1046 18 18V7M6 7H5M6 7H8M18 7H19M18 7H16M10 11V16M14 11V16M8 7V5C8 3.89543 8.89543 3 10 3H14C15.1046 3 16 3.89543 16 5V7M8 7H16" stroke="#4e4e4e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
        </span>

        
      </div>

    </article>
  </div>

  <TaskForm
    :task="task"
    v-model:is-open="isOpen"
    :mode="'edit'"
    @update:isOpen="isOpen = $event"
    @save-task="updateTask"
  />
</template>


<style scoped>
article {
  border: rgb(235, 235, 235) 1px solid;
  border-radius: 8px;
  padding: 15px;
  background-color: white;
  min-width: 250px;
  box-shadow: 0px 0px 4px 1px rgb(129 129 129 / 10%);


  &.open:hover {
        background: rgb(129 129 129 / 20%);
        transition: all 0.3s ease;
        cursor: pointer;
    }
}

h2 {
  font-family: var(--ff-base);
  color: var(--clr-primary-2);
  margin-bottom: 12px;
  text-align: center;
}

div.wrapper {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 5px;
}

div.title-delete-wrapper {
    display: flex;
    align-items: center;
    gap: 5px;
    width: 100%;
}

svg.checked-icon {
    width: 15px;
}

svg.unchecked-icon {
    width: 10px;
}

span.remove {
  z-index: 100;
  & svg {
      width: 18px;
      transform: translateX(10px);
      opacity: 0;
      transition: all 0.3s ease;
      margin-left: 5px;
  }
}

.edit-icon {
    width: 18px;
    transform: translateX(10px);
    opacity: 0;
    transition: all 0.3s ease;
    margin-left: auto;
} 

article:hover > div.wrapper > .edit-icon,
article:hover > div.wrapper > .remove svg {
    transform: translateX(0);
    opacity: 1;
}

p.task-title {
    margin: 0px;
    font-family: var(--ff-base);
}
</style>
