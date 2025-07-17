'use client';

import { CheckSquare, PlusCircle } from 'lucide-react';
import React, { useState, useMemo } from 'react';

import { TaskDetailDrawer } from '@/components/tasks/task-detail-drawer';
import { TaskFormDrawer } from '@/components/tasks/task-form-drawer';
import { TasksList } from '@/components/tasks/tasks-list';
import { Button, Card } from '@/components/ui';
import { Skeleton } from '@/components/ui/skeleton';
import { TaskFilterParams } from '@/lib/api/task-service';
import { useTasks, useTaskMutations } from '@/lib/hooks/use-tasks';

interface PropertyTasksTabProps {
  propertyId: number;
  property?: any;
}

export function PropertyTasksTab({ propertyId, property }: PropertyTasksTabProps) {
  // Task-related state
  const [selectedTask, setSelectedTask] = useState<any>(null);
  const [isTaskFormOpen, setIsTaskFormOpen] = useState(false);
  const [isTaskDetailOpen, setIsTaskDetailOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);
  const [taskFilters, setTaskFilters] = useState({
    is_completed: false,
    search: '',
    assignee_id: undefined,
    priority: undefined,
  });

  // Add tasks functionality - memoize filter params to prevent infinite loops
  const filterParams: TaskFilterParams = useMemo(
    () => ({
      operation_id: propertyId ? String(propertyId) : undefined,
    }),
    [propertyId]
  );

  const { data: taskData, isLoading: isTasksLoading } = useTasks(filterParams);
  const { updateTask, deleteTask } = useTaskMutations();

  // Get property tasks
  const propertyTasks = taskData?.results || [];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-medium text-secondary-900 dark:text-white flex items-center">
          <CheckSquare className="mr-2 text-primary-500" size={20} />
          Tâches de {property?.name}
        </h3>
        <Button onClick={() => setIsTaskFormOpen(true)} className="flex items-center gap-2">
          <PlusCircle size={16} />
          Créer une tâche
        </Button>
      </div>

      <div className="mb-4">
        <p className="text-secondary-500 dark:text-secondary-400">
          Gérez toutes les tâches et actions liées à cette propriété
        </p>
      </div>

      {/* Tasks Statistics */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 xl:grid-cols-4 mb-6">
        <Card className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-secondary-500">Tâches actives</p>
              {isTasksLoading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <h3 className="text-2xl font-bold">
                  {propertyTasks.filter(t => !t.is_completed).length}
                </h3>
              )}
            </div>
            <CheckSquare className="h-8 w-8 text-primary-600/80" />
          </div>
        </Card>

        <Card className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-secondary-500">Tâches terminées</p>
              {isTasksLoading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <h3 className="text-2xl font-bold">
                  {propertyTasks.filter(t => t.is_completed).length}
                </h3>
              )}
            </div>
            <CheckSquare className="h-8 w-8 text-success-600/80" />
          </div>
        </Card>

        <Card className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-secondary-500">En retard</p>
              {isTasksLoading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <h3 className="text-2xl font-bold">
                  {
                    propertyTasks.filter(
                      t =>
                        !t.is_completed && t.due_date && new Date(t.due_date) < new Date()
                    ).length
                  }
                </h3>
              )}
            </div>
            <CheckSquare className="h-8 w-8 text-error-600/80" />
          </div>
        </Card>

        <Card className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-secondary-500">Aujourd'hui</p>
              {isTasksLoading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <h3 className="text-2xl font-bold">
                  {
                    propertyTasks.filter(
                      t =>
                        !t.is_completed &&
                        t.due_date &&
                        new Date(t.due_date).toDateString() === new Date().toDateString()
                    ).length
                  }
                </h3>
              )}
            </div>
            <CheckSquare className="h-8 w-8 text-warning-600/80" />
          </div>
        </Card>
      </div>

      {/* Tasks Content */}
      <div className="bg-white dark:bg-secondary-800 border border-secondary-200 dark:border-secondary-700 rounded-lg shadow-sm">
        <div className="p-6">
          {isTasksLoading ? (
            <div className="flex items-center justify-center h-48">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
            </div>
          ) : propertyTasks.length === 0 ? (
            // Empty state when no tasks exist
            <div className="text-center py-12">
              <div className="text-secondary-400 mb-4">
                <CheckSquare className="w-16 h-16 mx-auto mb-4" />
              </div>
              <h3 className="text-lg font-medium text-secondary-900 dark:text-white mb-2">
                Aucune tâche pour cette propriété
              </h3>
              <p className="text-secondary-500 dark:text-secondary-400 mb-6 max-w-md mx-auto">
                Créez votre première tâche pour commencer à organiser la gestion de cette
                propriété.
              </p>
              <Button
                onClick={() => setIsTaskFormOpen(true)}
                className="flex items-center gap-2"
              >
                <PlusCircle size={16} />
                Créer votre première tâche
              </Button>
            </div>
          ) : (
            // Tasks list when tasks exist
            <TasksList
              filterParams={{
                ...taskFilters,
                operation_id: propertyId.toString(),
              }}
              onSelectTask={task => {
                setSelectedTask(task);
                setIsTaskDetailOpen(true);
              }}
            />
          )}
        </div>
      </div>

      {/* Task Form Drawer */}
      <TaskFormDrawer
        isOpen={isTaskFormOpen}
        onClose={() => setIsTaskFormOpen(false)}
        onSave={task => {
          // Handle task save logic here
          console.log('Task saved:', task);
          setIsTaskFormOpen(false);
        }}
        task={editingTask}
        mode={editingTask ? 'edit' : 'create'}
      />

      {/* Task Detail Drawer */}
      {selectedTask && (
        <TaskDetailDrawer
          isOpen={isTaskDetailOpen}
          onClose={() => {
            setIsTaskDetailOpen(false);
            setSelectedTask(null);
          }}
          onEdit={task => {
            setEditingTask(task);
            setIsTaskFormOpen(true);
            setIsTaskDetailOpen(false);
          }}
          task={selectedTask}
        />
      )}
    </div>
  );
} 