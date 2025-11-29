Wazuh server cluster
- load balance
- high availability
- The Wazuh agent registration details, shared configuration, CDB list, custom SCA policies, custom decoders, and rules are synchronized from the master to the workers, ensuring that all nodes have the same configuration and rulesets. During synchronization, every version of these files on the worker node is overwritten with the files from the master node.