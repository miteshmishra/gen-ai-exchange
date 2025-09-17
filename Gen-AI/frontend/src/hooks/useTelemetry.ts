import { useCallback, useEffect, useRef } from 'react';

interface TelemetryEvent {
  type: string;
  component: string;
  action: string;
  taskId?: string;
  taskTimeMs?: number;
  metadata?: Record<string, any>;
}

interface UseTelemetryOptions {
  component: string;
  taskId?: string;
  debounceMs?: number;
}

export const useTelemetry = ({
  component,
  taskId,
  debounceMs = 1000,
}: UseTelemetryOptions) => {
  const taskStartTime = useRef<number | null>(null);

  // Send telemetry event to backend (currently disabled)
  const sendTelemetry = useCallback(
    (event: TelemetryEvent) => {
      // Telemetry API endpoint not implemented yet
      console.log('Telemetry event:', event);
    },
    []
  );

  // Track user interactions
  const trackEvent = useCallback(
    (action: string, metadata?: Record<string, any>) => {
      const event: TelemetryEvent = {
        type: 'interaction',
        component,
        action,
        taskId,
        metadata,
      };
      sendTelemetry(event);
    },
    [component, taskId, sendTelemetry]
  );

  // Track task start
  const startTask = useCallback(() => {
    taskStartTime.current = Date.now();
    trackEvent('task_start');
  }, [trackEvent]);

  // Track task completion
  const completeTask = useCallback(
    (success: boolean, metadata?: Record<string, any>) => {
      if (taskStartTime.current) {
        const taskTimeMs = Date.now() - taskStartTime.current;
        trackEvent('task_complete', {
          ...metadata,
          success,
          taskTimeMs,
        });
        taskStartTime.current = null;
      }
    },
    [trackEvent]
  );

  // Track rage clicks
  const clickCount = useRef<{ [key: string]: number }>({});
  const lastClickTime = useRef<{ [key: string]: number }>({});

  const trackClick = useCallback(
    (elementId: string) => {
      const now = Date.now();
      const timeSinceLastClick = now - (lastClickTime.current[elementId] || 0);

      // Reset counter if more than 1 second between clicks
      if (timeSinceLastClick > 1000) {
        clickCount.current[elementId] = 1;
      } else {
        clickCount.current[elementId] = (clickCount.current[elementId] || 0) + 1;

        // Detect rage clicking (more than 3 clicks in quick succession)
        if (clickCount.current[elementId] === 3) {
          trackEvent('rage_click', { elementId });
        }
      }

      lastClickTime.current[elementId] = now;
    },
    [trackEvent]
  );

  // Track page visibility and focus
  useEffect(() => {
    const handleVisibilityChange = () => {
      trackEvent(document.hidden ? 'page_hide' : 'page_show');
    };

    const handleFocus = () => {
      trackEvent('window_focus');
    };

    const handleBlur = () => {
      trackEvent('window_blur');
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('focus', handleFocus);
    window.addEventListener('blur', handleBlur);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('focus', handleFocus);
      window.removeEventListener('blur', handleBlur);
    };
  }, [trackEvent]);

  return {
    trackEvent,
    startTask,
    completeTask,
    trackClick,
  };
};
