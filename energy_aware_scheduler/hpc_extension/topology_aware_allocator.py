class TopologyAwareAllocator:
    def __init__(self, system_topology):
        self.topology = system_topology  # Represents node connections

    def allocate(self, task, available_nodes):
        # Find nodes that minimize network distance for task's communication pattern
        if hasattr(task.communication_pattern, 'is_nearest_neighbor') and task.communication_pattern.is_nearest_neighbor():
            return self._allocate_contiguous_nodes(task, available_nodes)
        elif hasattr(task.communication_pattern, 'is_all_to_all') and task.communication_pattern.is_all_to_all():
            return self._allocate_high_bandwidth_nodes(task, available_nodes)
        else:
            return self._allocate_default(task, available_nodes)

    def _allocate_contiguous_nodes(self, task, available_nodes):
        # Simplified: allocate first contiguous block of nodes
        return available_nodes[:task.computation_profile.get('required_nodes', 1)]

    def _allocate_high_bandwidth_nodes(self, task, available_nodes):
        # Simplified: allocate nodes with highest bandwidth (placeholder)
        return available_nodes[:task.computation_profile.get('required_nodes', 1)]

    def _allocate_default(self, task, available_nodes):
        # Default allocation strategy
        return available_nodes[:task.computation_profile.get('required_nodes', 1)]
