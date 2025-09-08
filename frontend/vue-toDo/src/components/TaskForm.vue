<script setup lang="ts">
import { ref, onMounted, type Ref, watch } from 'vue'
import { type Task } from '@/models/task';

interface Props {
  task: Task,
  isOpen: boolean,
  mode: 'create' | 'edit',
};

const props = defineProps<Props>();

// Create a copy of the task data for editing
const taskCopy = ref({ ...props.task });
console.log("TASK IN FORM: ", taskCopy.value);

const minDueDate = ref(props.task.created_at || new Date().toISOString().split('T')[0]);


// Function to handle date input changes
const handleDateChange = (event: Event) => {
  const inputValue = (event.target as HTMLInputElement).value;
  console.log("Date input changed to:", inputValue);
  taskCopy.value.dueDate = inputValue;
};

const saveTask = async () => {
  // Create a copy of the task data to ensure we don't modify the reactive reference
  const taskToSave = { ...taskCopy.value };
  
  // Ensure dueDate is in the correct format
  if (taskToSave.dueDate) {
    // It should already be in YYYY-MM-DD format from the date input
    console.log("Saving task with due date:", taskToSave.dueDate);
  }
  
  emit('saveTask', taskToSave);
  closeForm();
}

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void;
  (e: 'saveTask', task: Task): void;
  (e: 'updateTask', task: Task): void;
}>()

function closeForm() {
  emit('update:isOpen', false)
}
</script>
 
<template>
  <section class="form-section" v-if="props.isOpen">
    <form @submit.prevent="saveTask">
        <article class="close">
          <label class="task-label" for="title">Title:</label>
          <input id="title" class="task-input" type="text" v-model="taskCopy.title" />

          <label class="task-label" for="description">Description:</label>
          <input id="description" class="task-input" type="text" v-model="taskCopy.description" />

          <label v-if="props.mode === 'edit'" class="task-label">Created at:</label>
          <p v-if="props.mode === 'edit'" class="created_date">{{ props.task.created_at }}</p>

          <label class="task-label">Status:</label>
          <span class="status-wrapper">
            <input class="task-input" type="checkbox" :checked="taskCopy.done" @change="taskCopy.done = !taskCopy.done" />
            <span class="status-desc" @click="taskCopy.done = !taskCopy.done">{{ taskCopy.done ? 'Completed' : 'Pending' }}</span>
          </span>

          <label class="task-label">Due Date:</label>
          <input class="task-input" type="date" v-model="taskCopy.dueDate" :min="minDueDate" @input="handleDateChange" />
          <p v-if="props.mode === 'edit'" class="date-hint">Minimum date is task creation date: {{ props.task.created_at }}</p>

          <label class="task-label">Owner:</label>
          <input class="task-input" type="text" v-model="taskCopy.owner" />

          <div class="buttons-wrapper">
              <button class="save" type="submit">Save</button>
              <button class="close" type="button" @click="closeForm">Close</button>
          </div>
        </article>
    </form>
  </section>
</template>

<style scoped>
.form-section {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
form {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    width: 700px;
    position: absolute;
    top: 10%
}

p.task-title {
    margin: 0px;
}

.task-label {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--clr-primary-4);
  margin: 10px 0 2px 0;
  display: block;
  font-family: var(--ff-base);
}

.task-input {
  font-size: 1.1rem;
  font-weight: 500;
  border: none;
  border-bottom: 1px solid var(--clr-primary-2);
  outline: none;
  width: 100%;
  margin: 10px 0px;
  background: transparent;
  padding: 2px 0;
  box-sizing: border-box;
}
span.status-wrapper {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    accent-color: var(--clr-primary-1);
    border-radius: 4px;
    margin: 10px 0px 20px;
    font-family: var(--ff-base);

  & label {
        margin: 0px;
  }
  & input {
    width: 15px;
    cursor: pointer;
    margin: 0px 5px 0px 0px;
  }
  & .status-desc {
    color: var(--clr-complementary-1);
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
  }
}

p.created_date {
  color: rgb(99, 99, 99);
  font-family: var(--ff-base);
}

p.date-hint {
  color: rgb(99, 99, 99);
  font-family: var(--ff-base);
  font-size: 0.8rem;
  font-style: italic;
  margin-top: -5px;
  margin-bottom: 10px;
}

p.date-selected {
  color: rgb(0, 128, 0);
  font-family: var(--ff-base);
  font-size: 0.9rem;
  margin-top: -5px;
  margin-bottom: 10px;
}

p.date-debug {
  color: rgb(128, 0, 0);
  font-family: var(--ff-base);
  font-size: 0.8rem;
  font-style: italic;
  margin-top: -5px;
  margin-bottom: 10px;
}
  
div.buttons-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
  margin-top: 15px;

  & button.delete {
    font-family: var(--ff-base);
    background-color: var(--clr-triad-1);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
        background-color: #dd0f00;
        transition: background-color 0.2s ease;
    }
  }
}

button.save {
    background-color: var(--clr-primary-1);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
    &:hover {
        background-color: var(--clr-primary-4);
        transition: background-color 0.2s ease;
    }
}
button.close {
    font-family: var(--ff-base);
    background-color: var(--clr-triad-1);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
        background-color: #dd0f00;
        transition: background-color 0.2s ease;
    }

}
</style>
