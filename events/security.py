def client_ip(request):
    # Safe to trust: Caddy overwrites X-Real-IP, and the app is only reachable through it.
    return request.META.get("HTTP_X_REAL_IP") or request.META["REMOTE_ADDR"]
