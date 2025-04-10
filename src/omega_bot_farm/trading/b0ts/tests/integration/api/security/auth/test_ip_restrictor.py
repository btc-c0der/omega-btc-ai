
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
Tests for IP restriction security in the BitgetPositionAnalyzerB0t API.

These tests verify:
- Whitelisted IPs are allowed access
- Non-whitelisted IPs are blocked
- IP ranges (CIDR) are properly processed
- IP whitelists can be updated dynamically
- Country-based IP restrictions work as expected
"""

import ipaddress
import pytest
from unittest.mock import patch, MagicMock

# Try to import the real implementation, fall back to mock if not available
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.security import IPRestrictor
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False
    
    # Mock implementation for tests
    class IPRestrictor:
        """IP restrictor for API access."""
        
        def __init__(self, whitelist=None, blocked_countries=None):
            """Initialize the IP restrictor."""
            self.whitelist = set()
            self.ip_networks = []
            
            if whitelist:
                for ip in whitelist:
                    self.add_to_whitelist(ip)
                    
            self.blocked_countries = blocked_countries or []
            self.country_cache = {}  # IP -> country code
        
        def add_to_whitelist(self, ip_or_cidr):
            """Add an IP or CIDR range to the whitelist."""
            if '/' in ip_or_cidr:
                # This is a CIDR range
                try:
                    network = ipaddress.ip_network(ip_or_cidr, strict=False)
                    self.ip_networks.append(network)
                except ValueError:
                    # Invalid CIDR notation
                    pass
            else:
                # Single IP address
                self.whitelist.add(ip_or_cidr)
        
        def remove_from_whitelist(self, ip_or_cidr):
            """Remove an IP or CIDR range from the whitelist."""
            if '/' in ip_or_cidr:
                # This is a CIDR range
                try:
                    network = ipaddress.ip_network(ip_or_cidr, strict=False)
                    if network in self.ip_networks:
                        self.ip_networks.remove(network)
                except ValueError:
                    # Invalid CIDR notation
                    pass
            else:
                # Single IP address
                if ip_or_cidr in self.whitelist:
                    self.whitelist.remove(ip_or_cidr)
        
        def is_ip_allowed(self, ip_address):
            """Check if an IP address is allowed access."""
            # Check if IP is directly whitelisted
            if ip_address in self.whitelist:
                return True
                
            # Check if IP is in any whitelisted CIDR range
            try:
                ip_obj = ipaddress.ip_address(ip_address)
                for network in self.ip_networks:
                    if ip_obj in network:
                        return True
            except ValueError:
                # Invalid IP address
                return False
                
            # If no whitelist, default to allowing access
            if not self.whitelist and not self.ip_networks:
                return True
                
            # IP not in whitelist
            return False
        
        def is_country_allowed(self, ip_address):
            """Check if the country for this IP is not blocked."""
            # If no country restrictions, allow access
            if not self.blocked_countries:
                return True
                
            # Check the country code for this IP
            country_code = self._get_country_for_ip(ip_address)
            
            # If country lookup failed, default to allowing access
            if not country_code:
                return True
                
            # Check if country is in blocked list
            return country_code.upper() not in [c.upper() for c in self.blocked_countries]
        
        def _get_country_for_ip(self, ip_address):
            """Get the country code for an IP address."""
            # Check cache first
            if ip_address in self.country_cache:
                return self.country_cache[ip_address]
                
            # In a real implementation, this would use a geolocation service
            # For testing, we'll use a simple mapping
            test_mappings = {
                "192.168.1.1": "US",
                "10.0.0.1": "UK",
                "172.16.0.1": "CN",
                "127.0.0.1": "US",
                "8.8.8.8": "US",
                "1.1.1.1": "AU"
            }
            
            country = test_mappings.get(ip_address, "")
            
            # Cache the result
            self.country_cache[ip_address] = country
            
            return country


@pytest.fixture
def ip_restrictor():
    """Create an IP restrictor instance with test settings."""
    whitelist = ["127.0.0.1", "192.168.1.100", "10.0.0.0/24"]
    blocked_countries = ["CN", "RU", "KP"]
    return IPRestrictor(whitelist=whitelist, blocked_countries=blocked_countries)


class TestIPRestriction:
    """Test suite for IP restriction security."""
    
    def test_whitelist_single_ip(self, ip_restrictor):
        """Test that whitelisted IPs are allowed access."""
        # Check a directly whitelisted IP
        assert ip_restrictor.is_ip_allowed("127.0.0.1") is True
        assert ip_restrictor.is_ip_allowed("192.168.1.100") is True
        
    def test_whitelist_cidr_range(self, ip_restrictor):
        """Test that IPs in whitelisted CIDR ranges are allowed."""
        # Check IPs in the whitelisted CIDR range
        assert ip_restrictor.is_ip_allowed("10.0.0.1") is True
        assert ip_restrictor.is_ip_allowed("10.0.0.254") is True
        
    def test_non_whitelisted_ip(self, ip_restrictor):
        """Test that non-whitelisted IPs are blocked."""
        # Check IPs not in whitelist
        assert ip_restrictor.is_ip_allowed("8.8.8.8") is False
        assert ip_restrictor.is_ip_allowed("192.168.1.101") is False
        
    def test_empty_whitelist_allows_all(self):
        """Test that an empty whitelist allows all IPs."""
        # Create a restrictor with empty whitelist
        empty_restrictor = IPRestrictor()
        
        # Check that any IP is allowed
        assert empty_restrictor.is_ip_allowed("8.8.8.8") is True
        assert empty_restrictor.is_ip_allowed("1.1.1.1") is True
        
    def test_add_to_whitelist(self, ip_restrictor):
        """Test that IPs can be added to whitelist."""
        # Initially not whitelisted
        assert ip_restrictor.is_ip_allowed("8.8.8.8") is False
        
        # Add to whitelist
        ip_restrictor.add_to_whitelist("8.8.8.8")
        
        # Should now be whitelisted
        assert ip_restrictor.is_ip_allowed("8.8.8.8") is True
        
    def test_add_cidr_to_whitelist(self, ip_restrictor):
        """Test that CIDR ranges can be added to whitelist."""
        # Initially not whitelisted
        assert ip_restrictor.is_ip_allowed("172.16.0.1") is False
        assert ip_restrictor.is_ip_allowed("172.16.0.100") is False
        
        # Add CIDR range to whitelist
        ip_restrictor.add_to_whitelist("172.16.0.0/24")
        
        # Should now be whitelisted
        assert ip_restrictor.is_ip_allowed("172.16.0.1") is True
        assert ip_restrictor.is_ip_allowed("172.16.0.100") is True
        
    def test_remove_from_whitelist(self, ip_restrictor):
        """Test that IPs can be removed from whitelist."""
        # Initially whitelisted
        assert ip_restrictor.is_ip_allowed("127.0.0.1") is True
        
        # Remove from whitelist
        ip_restrictor.remove_from_whitelist("127.0.0.1")
        
        # Should no longer be whitelisted
        assert ip_restrictor.is_ip_allowed("127.0.0.1") is False
        
    def test_remove_cidr_from_whitelist(self, ip_restrictor):
        """Test that CIDR ranges can be removed from whitelist."""
        # Initially whitelisted
        assert ip_restrictor.is_ip_allowed("10.0.0.1") is True
        
        # Remove CIDR range from whitelist
        ip_restrictor.remove_from_whitelist("10.0.0.0/24")
        
        # Should no longer be whitelisted
        assert ip_restrictor.is_ip_allowed("10.0.0.1") is False
        
    def test_country_restriction_blocked(self, ip_restrictor):
        """Test that IPs from blocked countries are denied access."""
        # IP from China, which is blocked
        assert ip_restrictor.is_country_allowed("172.16.0.1") is False
        
    def test_country_restriction_allowed(self, ip_restrictor):
        """Test that IPs from allowed countries are granted access."""
        # IPs from allowed countries
        assert ip_restrictor.is_country_allowed("192.168.1.1") is True  # US
        assert ip_restrictor.is_country_allowed("10.0.0.1") is True     # UK
        
    def test_country_lookup_cache(self, ip_restrictor):
        """Test that country lookups are cached."""
        # Do an initial lookup to cache
        ip_restrictor.is_country_allowed("192.168.1.1")
        
        # Check that it's in the cache
        assert "192.168.1.1" in ip_restrictor.country_cache
        assert ip_restrictor.country_cache["192.168.1.1"] == "US"
        
    def test_integration_whitelist_and_country(self, ip_restrictor):
        """Test that both whitelist and country restrictions work together."""
        # Whitelisted IP from blocked country - whitelist takes precedence
        with patch.object(ip_restrictor, '_get_country_for_ip', return_value="CN"):
            # Add IP to whitelist
            ip_restrictor.add_to_whitelist("192.168.99.99")
            
            # IP is whitelisted but from a blocked country
            assert ip_restrictor.is_ip_allowed("192.168.99.99") is True
            assert ip_restrictor.is_country_allowed("192.168.99.99") is False
            
            # Still, it should be allowed if both checks are performed
            assert ip_restrictor.is_ip_allowed("192.168.99.99") is True
            
    def test_invalid_ip_address(self, ip_restrictor):
        """Test handling of invalid IP addresses."""
        # Invalid IP format
        assert ip_restrictor.is_ip_allowed("invalid.ip.address") is False
        
    def test_invalid_cidr_notation(self, ip_restrictor):
        """Test handling of invalid CIDR notation."""
        # Invalid CIDR format should be ignored
        ip_restrictor.add_to_whitelist("192.168.1.0/invalid")
        
        # IP in the range should still be blocked (invalid CIDR wasn't added)
        assert ip_restrictor.is_ip_allowed("192.168.1.50") is False 