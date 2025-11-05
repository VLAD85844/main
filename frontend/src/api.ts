import type { Task, TaskStatus } from './types'

const BASE = '/api/tasks'

export async function fetchTasks(status?: TaskStatus): Promise<Task[]> {
  const url = new URL(BASE, window.location.origin)
  if (status) url.searchParams.set('status', status)
  const res = await fetch(url.toString())
  if (!res.ok) throw new Error('Failed to fetch tasks')
  return res.json()
}

export async function createTask(input: { title: string; description?: string }): Promise<Task> {
  const res = await fetch(BASE + '/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  })
  if (!res.ok) throw new Error('Failed to create task')
  return res.json()
}

export async function updateTask(id: number, data: Partial<Pick<Task, 'title'|'description'|'status'>>): Promise<Task> {
  const res = await fetch(`${BASE}/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!res.ok) throw new Error('Failed to update task')
  return res.json()
}

export async function deleteTask(id: number): Promise<void> {
  const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete task')
}


