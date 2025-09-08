export interface Task {
  id: string
  title: string
  done: boolean
  listId: string
  description?: string
  created_at: string
  checklist?: string[]
  owner?: string
  dueDate?: string | null
  order: number
}