export type TaskStatus = 'pending' | 'in_progress' | 'done'

export interface Task {
  id: number
  title: string
  description?: string | null
  status: TaskStatus
  created_at: string
}


