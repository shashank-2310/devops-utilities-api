import psutil

def get_system_metrics():
    """
        This API gets the System Metrics(CPU, Memory, Disk, System Health)
        Based on below configurable Thresholds
    """
    #Thresholds
    cpu_threshold = 50
    cpu_critical = 85
    
    memory_threshold = 60
    memory_critical = 85
    
    disk_threshold = 60
    disk_critical = 85
    
    #Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    
    #Helper function to determine status
    def get_status(usage, threshold, critical):
        if usage < threshold:
            return "Healthy"
        elif usage < critical:
            return "Warning"
        else:
            return "Unhealthy"
    
    #Individual usage status
    cpu_status = get_status(cpu_usage, cpu_threshold, cpu_critical)
    memory_status = get_status(memory_usage, memory_threshold, memory_critical)
    disk_status = get_status(disk_usage, disk_threshold, disk_critical)
    
    #Overall system status
    all_statuses = [cpu_status, memory_status, disk_status]
    if "Unhealthy" in all_statuses:
        system_status = "Unhealthy"
    elif "Warning" in all_statuses:
        system_status = "Warning"
    else:
        system_status = "Healthy"
    
    return {
        "cpu_percentage" : cpu_usage,
        "memory_percentage" : memory_usage,
        "disk_percentage" : disk_usage,
        "system_status": system_status
    }
    