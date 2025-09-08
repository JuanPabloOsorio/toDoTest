<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createList, getLists } from '@/api/calls/list/listAPICalls'
import { type TaskList } from '@/models/list';

const emit = defineEmits(['listAdded'])
const createNewList = ref(false);
const existingLists = ref<TaskList[]>([]);

// Get current lists to determine the next order
onMounted(async () => {
  try {
    existingLists.value = await getLists();
  } catch (error) {
    console.error('Error fetching lists:', error);
  }
});

const newList: TaskList = {
  id: '',
  name: "New List",
  order: 0
}

const saveList = async () => {
  // Set the new list order to the end of the current lists
  newList.order = existingLists.value.length;
  
  const result = await createList(newList);
  createNewList.value = false;
  console.log('Saving list:', newList);
  
  // Add the created list to our array for future order calculations
  if (result) {
    existingLists.value.push(result);
  }
  
  // Reset the newList name for next time
  newList.name = "New List";
  
  // Emit event to parent component to refresh the lists
  emit('listAdded');
}
</script>

<template>
    <article @click="createNewList = true">
      <span v-if="!createNewList">
        <svg class="add-icon" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>plus</title> <desc>Created with Sketch Beta.</desc> <defs> </defs> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage"> <g id="Icon-Set-Filled" sketch:type="MSLayerGroup" transform="translate(-362.000000, -1037.000000)" fill="#78B2F0"> <path d="M390,1049 L382,1049 L382,1041 C382,1038.79 380.209,1037 378,1037 C375.791,1037 374,1038.79 374,1041 L374,1049 L366,1049 C363.791,1049 362,1050.79 362,1053 C362,1055.21 363.791,1057 366,1057 L374,1057 L374,1065 C374,1067.21 375.791,1069 378,1069 C380.209,1069 382,1067.21 382,1065 L382,1057 L390,1057 C392.209,1057 394,1055.21 394,1053 C394,1050.79 392.209,1049 390,1049" id="plus" sketch:type="MSShapeGroup"> </path> </g> </g> </g></svg>
        Add List
      </span>

      <span v-else class="wrapper">
        <input v-model="newList.name" />

        <div class="buttons-wrapper">
          <button @click.stop="saveList" class="add">
            Add List
          </button>

          <button @click.stop="createNewList = false" class="remove">
            Cancel
          </button>
        </div>
      </span>
    </article>

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
  height: 50px;
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