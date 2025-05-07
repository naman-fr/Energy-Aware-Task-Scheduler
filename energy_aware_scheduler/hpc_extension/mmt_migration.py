import logging

logger = logging.getLogger(__name__)

class MMTMigration:
    def __init__(self):
        pass

    def calculate_migration_time(self, vm_ram_usage, network_bandwidth):
        if network_bandwidth == 0:
            return float('inf')
        return vm_ram_usage / network_bandwidth

    def select_vms_to_migrate(self, over_utilized_hosts, host_vm_map, host_network_bandwidth):
        """
        over_utilized_hosts: list of host ids that are over-utilized
        host_vm_map: dict mapping host id to list of VMs with their RAM usage
        host_network_bandwidth: dict mapping host id to available network bandwidth
        Returns dict mapping host id to list of VMs selected for migration
        """
        migration_plan = {}
        for host_id in over_utilized_hosts:
            vms = host_vm_map.get(host_id, [])
            bandwidth = host_network_bandwidth.get(host_id, 0)
            # Sort VMs by migration time ascending
            vms_sorted = sorted(vms, key=lambda vm: self.calculate_migration_time(vm['ram_usage'], bandwidth))
            migration_plan[host_id] = vms_sorted
            logger.info(f"Host {host_id} migration plan: {[vm['id'] for vm in vms_sorted]}")
        return migration_plan

    def migrate_vms(self, migration_plan, target_hosts):
        """
        Perform migration of VMs according to the plan to target hosts.
        This is a placeholder for actual migration logic.
        """
        for src_host, vms in migration_plan.items():
            for vm in vms:
                # Find suitable target host (simplified)
                for tgt_host in target_hosts:
                    if tgt_host != src_host:
                        logger.info(f"Migrating VM {vm['id']} from {src_host} to {tgt_host}")
                        break
