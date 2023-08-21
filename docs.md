## UserAccessLevel
Enumeration representing different access levels for users in an ERP system.

    1. Superuser/Administrator: This is the highest level of access. 
        Superusers or administrators have complete control over the ERP system. 
        They can configure settings, add or remove users, assign roles, and access all 
        modules and data.

    2. Power User/Manager: Power users often have more privileges than regular users. 
        They can perform advanced tasks, generate reports, manage data within their departments, 
        and sometimes have limited administrative functions.

    3. Functional/User Role Access: Different functional roles within the organization 
        may have specific access levels tailored to their job requirements. These roles
        could include roles like finance, sales, procurement, inventory management, etc. 
        Users with functional roles can access and manipulate data relevant to their area 
        of responsibility.

    4. Read-Only/User: These users can view data and reports within the ERP system, but
        they do not have permission to modify or enter new data. This access level is 
        suitable for employees who need information for decision-making but do not need 
        to directly interact with the system.

    5. Data Entry/Transaction User: Users with this access level can enter and modify 
        data within specific modules or areas. They have limited access rights and are  
        primarily responsible for data entry and basic updates.

    6. External/Supplier/Customer: ERP systems may provide limited access to external 
        stakeholders such as suppliers and customers. This could allow them to view their 
        orders, invoices, and relevant information without having access to the entire system.

    7. Restricted Access: Some ERP systems allow for highly restricted access, granting 
        users permission to specific data or functions only. This level of access is often 
        used to ensure data security and compliance.

    8. Workflow/Approval User: These users have access to specific workflows or approval 
        processes within the ERP system. They review and approve/reject requests, such as 
        purchase orders or expense claims.

    9. Reporting/User Analytics: This access level is designed for users who primarily use 
        the ERP system for generating and analyzing reports, graphs, and performance indicators.

    9. Audit/User Activity: In some cases, there might be users or roles specifically focused 
        on monitoring and auditing user activity within the ERP system to ensure compliance 
        and security.

- different users have different acces depending on profile.access_level and 
profile.access_department
- some apps need specific access_department
    - wms: warehouse