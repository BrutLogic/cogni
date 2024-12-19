class Agentix:
    """Facade to a lot of moving parts
    """
    
    @staticmethod
    def all_endpoints_full() -> str:
        """Meant to be use by gen1 agents.
        return all the endpoints with internal state
        """

    @staticmethod
    def all_pages_full() -> str:
        """Returns all the pages with their full configurations."""
        from agentix.wrappers import Page
        pages_info = []
        for name, page in Page.items():
            pages_info.append(f"Page {name}: Template - {page.template}, CSS - {page.css}, JS - {page.js}")
        return "\n".join(pages_info)

    @staticmethod
    def all_components_full() -> str:
        """Returns all the components with their full configurations."""
        # This method would similarly enumerate all components, similar to all_pages_full.
        # Implementation would depend on how components are structured and stored.
        return "Components listing and their configurations."

    @staticmethod
    def all_functions_full() -> str:
        """Returns all the functions with their full configurations."""
        from agentix.wrappers import Func
        functions_info = []
        for name, func in Func.items():
            functions_info.append(f"Function {name}: Code - {func.code}")
        return "\n".join(functions_info)

    @staticmethod
    def all_entities_full() -> str:
        """Returns all the entities with their full configurations."""
        # This method would enumerate all entities, similar to all_pages_full.
        # Implementation would depend on how entities are structured and stored.
        return "Entities listing and their configurations."
