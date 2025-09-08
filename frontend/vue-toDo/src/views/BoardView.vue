<script setup lang="ts">
import List from '@/components/List.vue';
import Header from '@/components/nav/Header.vue';
import AddListButton from '@/components/AddList.vue';
import { type TaskList } from '@/models/list';
import { getLists, updateAllListsOrder } from '@/api/calls/list/listAPICalls';
import { ref, onMounted, getCurrentInstance } from 'vue';
import { vDraggable } from 'vue-draggable-plus'; // directive import

const lists = ref<TaskList[]>([]);

// Function to fetch all lists
const fetchLists = async () => {
  try {
    const fetchedLists = await getLists();
    // Sort the lists by order before assigning them
    lists.value = fetchedLists.sort((a, b) => (a.order || 0) - (b.order || 0));
    console.log('Fetched and sorted lists:', lists.value);
  } catch (error) {
    console.error('Error fetching lists:', error);
  }
}

// Handle list deletion event
const handleListDeleted = (listId: string) => {
  // Remove the deleted list from the local array
  lists.value = lists.value.filter(list => list.id !== listId);
}

onMounted(async () => {
  await fetchLists();
})

// Register the directive locally on the app instance (minimal change)
const inst = getCurrentInstance();
if (inst) {
  // Register v-draggable directive so template can use v-draggable
  inst.appContext.app.directive('draggable', vDraggable);
}

// Drag end callback (will be called by Sortable via the directive options)
const onDragEnd = async (evt: any) => {
  const { oldIndex, newIndex } = evt
  if (oldIndex === newIndex) return

  console.log(`List dragged from index ${oldIndex} to ${newIndex}`)

  const moved = [...lists.value]
  const item = moved.splice(oldIndex, 1)[0]
  moved.splice(newIndex, 0, item)

  // reasign the new positition
  moved.forEach((l, i) => { l.order = i })

  lists.value = moved


  try {
    const result = await updateAllListsOrder(lists.value)
    if (result) {
      console.log('All lists order updated successfully')
    } else {
      console.error('Failed to update list orders')
      await fetchLists()
    }
  } catch (error) {
    console.error('Error updating lists order:', error)
    await fetchLists()
  }
}
</script>


<template>
  <Header></Header>
  <section class="board-view">
    <!--
      English comment: use the directive form. Bind the reactive array and options.
      v-draggable expects [listRef, options]. We pass onEnd handler in options.
    -->
    <div v-draggable="[lists, { animation: 150, onEnd: onDragEnd }]" class="board-draggable">
      <List 
        v-for="taskList in lists" 
        :key="taskList.id" 
        :taskList="taskList"
        @list-deleted="handleListDeleted"
      ></List>
    </div>

    <AddListButton @list-added="fetchLists"></AddListButton>

  </section>
</template>

<style scoped>

section.board-view {
  display: flex;
}

/* keep board-draggable styling so lists lay out horizontally */
.board-draggable {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
</style>
