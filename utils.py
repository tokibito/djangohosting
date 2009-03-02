SEP_HOSTNAME = ':'
SEP_DOMAIN = '.'
HTTP_PORT = 80

class HostnameError(Exception):
    pass

def split_hostname(hostname):
    if hostname.count(SEP_HOSTNAME) > 1:
        raise HostnameError
    if SEP_HOSTNAME in hostname:
        return hostname.split(SEP_HOSTNAME)
    return hostname, HTTP_PORT

def split_domain(domain):
    if SEP_HOSTNAME in domain:
        raise HostnameError
    return domain.split(SEP_DOMAIN)

def split_subdomain(base, domain):
    name = domain[:-len(base)]
    if name.endswith(SEP_DOMAIN):
        return name[:-1]
    return name
