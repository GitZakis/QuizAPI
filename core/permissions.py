from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Επιτρέπει μόνο σε admin-καθηγητές να κάνουν τροποποίηση (POST, PUT, DELETE).
    Όλοι οι άλλοι έχουν μόνο read (GET, HEAD, OPTIONS).
    """
    def has_object_permission(self, request, view, obj):
        # Αν είναι GET, HEAD ή OPTIONS => επιτρέπεται πάντα
        if request.method in permissions.SAFE_METHODS:
            return True
        # Διαφορετικά, πρέπει να είναι ο user που το δημιουργησε.
        return obj.created_by == request.user
