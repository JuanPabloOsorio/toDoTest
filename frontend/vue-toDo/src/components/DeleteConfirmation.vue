  
<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ ItemId: string; ItemType: string, openDeleteConfirmationPopUp: boolean }>();
const emit = defineEmits(['confirm', 'cancel'])

const confirmDeleteElement = (ItemId: string) => {
  emit('confirm', ItemId);
}

const cancelDeleteElement = () => {
  emit('cancel');
}


</script>
  

<template>
  <section v-if="openDeleteConfirmationPopUp" class="delete-list-modal">
    <div class="delete-list-content">
      <h3>Are you sure you want to delete this {{props.ItemType}}?</h3>
      <p>This action cannot be undone.</p>
      <div class="buttons-wrapper">
        <button @click="confirmDeleteElement(props.ItemId);" class="confirm-delete">
          Yes,
        </button>
        <button @click="cancelDeleteElement" class="cancel-delete">
          Cancel
        </button>
      </div>
    </div>
  </section>
</template>
  
  
  
  
<style scoped>

section.delete-list-modal {
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

    & .delete-list-content {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      text-align: center;
      max-width: 400px;
      width: 90%;

      & h3 {
        margin-top: 0;
        color: rgb(199, 38, 38);
        font-family: var(--ff-base);
      }
      & p {
        color: var(--clr-primary-3);
        font-family: var(--ff-base);
        font-weight: bold;
      }
      & .buttons-wrapper {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
      }

      & .confirm-delete {
          color: white;
          font-family: var(--ff-base);
          background: var(--clr-primary-1);
          border: none;
          border-radius: 5px;
          padding: 7px 10px;
          cursor: pointer;
      }
      & .cancel-delete {
          color: var(--clr-primary-1);
          font-family: var(--ff-base);
          background: white;
          border: 1px solid var(--clr-primary-1);
          border-radius: 5px;
          padding: 7px 10px;
          cursor: pointer;
      }
    }
  }
</style>