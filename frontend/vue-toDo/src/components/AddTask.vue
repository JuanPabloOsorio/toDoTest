<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createAPITask } from '@/api/calls/task/taskAPICalls'
import { getTasksOfList } from '@/api/calls/list/listAPICalls'
import { type Task } from '@/models/task';
import TaskForm from './TaskForm.vue';

const props = defineProps<{listId: string}>();
const isTaskFormOpen = ref(false);
const emit = defineEmits(['taskAdded'])
const createNewTask = ref(false);
const tasksInList = ref<Task[]>([]);

// Get current tasks in the list to determine the next order
onMounted(async () => {
  try {
    tasksInList.value = await getTasksOfList(props.listId);
  } catch (error) {
    console.error('Error fetching tasks for list:', error);
  }
});

const newTask: Task = {
  id: '',
  title: "New Task",
  done: false,
  listId: props.listId,
  description: '',
  created_at: '',
  checklist: [''],
  owner: '',
  dueDate: null,
  order: 0
}

const submitTask = async (taskToCreate: Task) => {
  // Set the order to be the last position in the list
  taskToCreate.order = tasksInList.value.length;
  
  const createdTask = await createAPITask(taskToCreate);
  createNewTask.value = false;
  console.log('Saving task:', createdTask);

  // Add the created task to our local list for future order calculations
  if (createdTask) {
    tasksInList.value.push(createdTask);
  }

  // Reset the newTask for next time
  newTask.title = "New Task";
  newTask.description = '';
  newTask.checklist = [''];
  newTask.owner = '';
  newTask.dueDate = '';

  // Emit event to parent component
  emit('taskAdded', createdTask);
}
</script>

<template>
    <article @click="isTaskFormOpen = true">
      <span>
        <svg class="add-icon" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>plus</title> <desc>Created with Sketch Beta.</desc> <defs> </defs> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage"> <g id="Icon-Set-Filled" sketch:type="MSLayerGroup" transform="translate(-362.000000, -1037.000000)" fill="#78B2F0"> <path d="M390,1049 L382,1049 L382,1041 C382,1038.79 380.209,1037 378,1037 C375.791,1037 374,1038.79 374,1041 L374,1049 L366,1049 C363.791,1049 362,1050.79 362,1053 C362,1055.21 363.791,1057 366,1057 L374,1057 L374,1065 C374,1067.21 375.791,1069 378,1069 C380.209,1069 382,1067.21 382,1065 L382,1057 L390,1057 C392.209,1057 394,1055.21 394,1053 C394,1050.79 392.209,1049 390,1049" id="plus" sketch:type="MSShapeGroup"> </path> </g> </g> </g></svg>
        Add a Task
      </span>
    </article>

    <TaskForm
    :task="newTask"
    :isOpen="isTaskFormOpen"
    :mode="'create'"
    @update:isOpen="isTaskFormOpen = $event"
    @save-task="submitTask"
    />


</template>

<style scoped>

article {
  display: flex;
  justify-content: center;
  align-items: center;
  border: rgb(235, 235, 235) 1px solid;
  border-radius: 8px;
  background-color: white;
  min-width: 250px;
  box-shadow: 0px 0px 4px 1px rgb(129 129 129 / 10%);
  height: 15px;
  align-self: flex-start;
  margin-top: 16px;
  color: var(--clr-primary-1);
  font-family: var(--ff-base);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  background: white;
  padding: 10px;


}

svg.add-icon {
    width: 15px;
    margin-right: 8px;
}

span.wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
 }

div.buttons-wrapper {
  display: flex;
  justify-content: flex-start;
  gap: 5px;
  margin-top: 5px;
}

button {
  cursor: pointer;
}
button.add {
  background-color: var(--clr-primary-1);
  border: none;
  color: white;
  border-radius: 5px;
  padding: 5px 10px;
}

button.remove {
  background-color: var(--clr-triad-1);
  border: none;
  color: white;
  border-radius: 5px;
  padding: 5px 10px;
}


</style>