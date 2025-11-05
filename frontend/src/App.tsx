import React, { useEffect, useMemo, useState } from 'react'
import { createTask, deleteTask, fetchTasks, updateTask } from './api'
import type { Task, TaskStatus } from './types'

function App() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [filter, setFilter] = useState<TaskStatus | 'all'>('all')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchTasks(filter === 'all' ? undefined : filter)
      setTasks(data)
    } catch (e) {
      setError('Не удалось загрузить задачи')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [filter])

  async function onAdd(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim()) return
    const newTask = await createTask({ title: title.trim(), description: description.trim() || undefined })
    setTitle('')
    setDescription('')
    if (filter === 'all' || filter === newTask.status) setTasks(prev => [newTask, ...prev])
  }

  async function onToggleStatus(t: Task) {
    const next: Record<TaskStatus, TaskStatus> = { pending: 'in_progress', in_progress: 'done', done: 'pending' }
    const updated = await updateTask(t.id, { status: next[t.status] })
    setTasks(prev => prev.map(x => (x.id === t.id ? updated : x)))
  }

  async function onDelete(id: number) {
    await deleteTask(id)
    setTasks(prev => prev.filter(x => x.id !== id))
  }

  const filtered = useMemo(() => tasks, [tasks])

  return (
    <div className="container">
      <h1>Задачи</h1>

      <form className="add-form" onSubmit={onAdd}>
        <input
          placeholder="Название"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <textarea
          placeholder="Описание (необязательно)"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button type="submit">Добавить</button>
      </form>

      <div className="toolbar">
        <div className="filters">
          {(['all', 'pending', 'in_progress', 'done'] as const).map(s => (
            <button
              key={s}
              className={filter === s ? 'active' : ''}
              onClick={() => setFilter(s)}
            >
              {s === 'all' ? 'Все' : s === 'pending' ? 'Ожидает' : s === 'in_progress' ? 'В работе' : 'Готово'}
            </button>
          ))}
        </div>
        {loading && <span className="muted">Загрузка...</span>}
        {error && <span className="error">{error}</span>}
      </div>

      <ul className="list">
        {filtered.map(t => (
          <li key={t.id} className={`item ${t.status}`}>
            <div className="item-main">
              <div className="item-head">
                <span className="badge">
                  {t.status === 'pending' ? 'Ожидает' : t.status === 'in_progress' ? 'В работе' : 'Готово'}
                </span>
                <h3>{t.title}</h3>
                <span className="spacer" />
              </div>
              {t.description ? <p>{t.description}</p> : null}
              <div className="item-actions">
                <button onClick={() => onToggleStatus(t)}>Статус</button>
                <button className="danger" onClick={() => onDelete(t.id)}>Удалить</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App


