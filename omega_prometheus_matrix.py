#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA ^PROMETHEUS^ MATRIX Monitoring System

A powerful CLI-based monitoring system for the OMEGA BTC AI platform with
foresight-driven monitoring, metrics collection, and system observability.

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0
"""

import os
import sys
import time
import asyncio
import logging
import psutil
import argparse
import json
import signal
import curses
import datetime
import socket
from typing import Dict, List, Any, Optional, Tuple, Set, Callable, Union
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='omega_prometheus_matrix.log'
)
logger = logging.getLogger('OMEGA_PROMETHEUS')

# ANSI Colors for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

class PrometheusMetric:
    """Base class for metrics collected by the OMEGA PROMETHEUS MATRIX"""
    
    def __init__(self, name: str, description: str, labels: Optional[Dict[str, str]] = None):
        self.name = name
        self.description = description
        self.labels = labels or {}
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "labels": self.labels,
            "timestamp": self.timestamp
        }

class GaugeMetric(PrometheusMetric):
    """Metric that represents a single numerical value that can go up and down"""
    
    def __init__(self, name: str, description: str, value: float = 0.0, labels: Optional[Dict[str, str]] = None):
        super().__init__(name, description, labels)
        self.value = value
    
    def set(self, value: float) -> None:
        """Set the gauge to a specific value"""
        self.value = value
        self.timestamp = time.time()
    
    def inc(self, amount: float = 1.0) -> None:
        """Increment the gauge by the given amount"""
        self.value += amount
        self.timestamp = time.time()
    
    def dec(self, amount: float = 1.0) -> None:
        """Decrement the gauge by the given amount"""
        self.value -= amount
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert gauge metric to dictionary representation"""
        base_dict = super().to_dict()
        base_dict["type"] = "gauge"
        base_dict["value"] = self.value
        return base_dict

class CounterMetric(PrometheusMetric):
    """Metric that represents a cumulative counter that only goes up"""
    
    def __init__(self, name: str, description: str, value: float = 0.0, labels: Optional[Dict[str, str]] = None):
        super().__init__(name, description, labels)
        self.value = value
    
    def inc(self, amount: float = 1.0) -> None:
        """Increment the counter by the given amount"""
        if amount < 0:
            raise ValueError("Counter can only be incremented by a positive value")
        self.value += amount
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert counter metric to dictionary representation"""
        base_dict = super().to_dict()
        base_dict["type"] = "counter"
        base_dict["value"] = self.value
        return base_dict

class HistogramMetric(PrometheusMetric):
    """Metric that samples observations and counts them in configurable buckets"""
    
    def __init__(self, name: str, description: str, buckets: List[float] = None, labels: Optional[Dict[str, str]] = None):
        super().__init__(name, description, labels)
        # Default buckets if none provided
        self.buckets = buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
        # Ensure +Inf is the last bucket
        if self.buckets[-1] != float('inf'):
            self.buckets.append(float('inf'))
        
        # Initialize bucket counters
        self.bucket_counts = {b: 0 for b in self.buckets}
        self.sum = 0.0
        self.count = 0
    
    def observe(self, value: float) -> None:
        """Record an observation in the histogram"""
        for bucket in self.buckets:
            if value <= bucket:
                self.bucket_counts[bucket] += 1
        
        self.sum += value
        self.count += 1
        self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert histogram metric to dictionary representation"""
        base_dict = super().to_dict()
        base_dict["type"] = "histogram"
        base_dict["buckets"] = {str(k): v for k, v in self.bucket_counts.items()}
        base_dict["sum"] = self.sum
        base_dict["count"] = self.count
        return base_dict

class MetricsRegistry:
    """Registry to store and manage all metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.last_collection_time = 0
    
    def register_metric(self, metric: PrometheusMetric) -> None:
        """Register a new metric in the registry"""
        key = f"{metric.name}_{','.join([f'{k}={v}' for k, v in sorted(metric.labels.items())])}"
        self.metrics[key] = metric
    
    def get_metric(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[PrometheusMetric]:
        """Retrieve a metric by name and labels"""
        labels = labels or {}
        key = f"{name}_{','.join([f'{k}={v}' for k, v in sorted(labels.items())])}"
        return self.metrics.get(key)
    
    def get_all_metrics(self) -> Dict[str, PrometheusMetric]:
        """Get all registered metrics"""
        return self.metrics
    
    def clear(self) -> None:
        """Clear all metrics from the registry"""
        self.metrics = {}
        
    def metrics_as_dict(self) -> Dict[str, Dict[str, Any]]:
        """Get all metrics as a dictionary of dictionaries"""
        return {k: m.to_dict() for k, m in self.metrics.items()}

class PrometheusCollector:
    """Base class for all metric collectors"""
    
    def __init__(self, registry: MetricsRegistry):
        self.registry = registry
        self.collection_interval = 60  # Default collection interval in seconds
        self.enabled = True
    
    async def collect(self) -> None:
        """Collect metrics - to be implemented by subclasses"""
        raise NotImplementedError("Collectors must implement collect() method")
    
    async def run(self) -> None:
        """Run the collector in a loop"""
        while self.enabled:
            try:
                await self.collect()
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
            
            await asyncio.sleep(self.collection_interval)
    
    def set_collection_interval(self, interval: int) -> None:
        """Set the collection interval in seconds"""
        self.collection_interval = interval 

class SystemCollector(PrometheusCollector):
    """Collector for system metrics (CPU, Memory, Disk)"""
    
    def __init__(self, registry: MetricsRegistry):
        super().__init__(registry)
        self.collection_interval = 5  # More frequent updates for system metrics
        
        # Initialize metrics
        self.cpu_usage = GaugeMetric(
            "system_cpu_usage", 
            "CPU usage percentage",
            labels={"host": socket.gethostname()}
        )
        self.memory_usage = GaugeMetric(
            "system_memory_usage",
            "Memory usage in percentage",
            labels={"host": socket.gethostname()}
        )
        self.memory_available = GaugeMetric(
            "system_memory_available",
            "Available memory in bytes",
            labels={"host": socket.gethostname()}
        )
        self.disk_usage = GaugeMetric(
            "system_disk_usage",
            "Disk usage percentage for root filesystem",
            labels={"host": socket.gethostname(), "path": "/"}
        )
        
        # Register metrics
        self.registry.register_metric(self.cpu_usage)
        self.registry.register_metric(self.memory_usage)
        self.registry.register_metric(self.memory_available)
        self.registry.register_metric(self.disk_usage)
    
    async def collect(self) -> None:
        """Collect system metrics"""
        # CPU usage
        self.cpu_usage.set(psutil.cpu_percent(interval=1))
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.percent)
        self.memory_available.set(memory.available)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        self.disk_usage.set(disk.percent)
        
        logger.debug(f"Collected system metrics: CPU: {self.cpu_usage.value}%, "
                    f"Memory: {self.memory_usage.value}%, Disk: {self.disk_usage.value}%")

class NetworkCollector(PrometheusCollector):
    """Collector for network metrics"""
    
    def __init__(self, registry: MetricsRegistry):
        super().__init__(registry)
        self.collection_interval = 10
        self.last_net_io = psutil.net_io_counters()
        self.last_collection_time = time.time()
        
        # Initialize metrics
        self.bytes_sent = CounterMetric(
            "network_bytes_sent",
            "Total bytes sent",
            labels={"host": socket.gethostname()}
        )
        self.bytes_recv = CounterMetric(
            "network_bytes_recv",
            "Total bytes received",
            labels={"host": socket.gethostname()}
        )
        self.packets_sent = CounterMetric(
            "network_packets_sent",
            "Total packets sent",
            labels={"host": socket.gethostname()}
        )
        self.packets_recv = CounterMetric(
            "network_packets_recv",
            "Total packets received",
            labels={"host": socket.gethostname()}
        )
        self.bytes_sent_per_sec = GaugeMetric(
            "network_bytes_sent_per_sec",
            "Bytes sent per second",
            labels={"host": socket.gethostname()}
        )
        self.bytes_recv_per_sec = GaugeMetric(
            "network_bytes_recv_per_sec",
            "Bytes received per second",
            labels={"host": socket.gethostname()}
        )
        
        # Register metrics
        self.registry.register_metric(self.bytes_sent)
        self.registry.register_metric(self.bytes_recv)
        self.registry.register_metric(self.packets_sent)
        self.registry.register_metric(self.packets_recv)
        self.registry.register_metric(self.bytes_sent_per_sec)
        self.registry.register_metric(self.bytes_recv_per_sec)
    
    async def collect(self) -> None:
        """Collect network metrics"""
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_collection_time
        
        # Update counters
        bytes_sent_diff = current_net_io.bytes_sent - self.last_net_io.bytes_sent
        bytes_recv_diff = current_net_io.bytes_recv - self.last_net_io.bytes_recv
        packets_sent_diff = current_net_io.packets_sent - self.last_net_io.packets_sent
        packets_recv_diff = current_net_io.packets_recv - self.last_net_io.packets_recv
        
        self.bytes_sent.inc(bytes_sent_diff)
        self.bytes_recv.inc(bytes_recv_diff)
        self.packets_sent.inc(packets_sent_diff)
        self.packets_recv.inc(packets_recv_diff)
        
        # Calculate rates
        self.bytes_sent_per_sec.set(bytes_sent_diff / time_diff if time_diff > 0 else 0)
        self.bytes_recv_per_sec.set(bytes_recv_diff / time_diff if time_diff > 0 else 0)
        
        # Store values for next collection
        self.last_net_io = current_net_io
        self.last_collection_time = current_time
        
        logger.debug(f"Collected network metrics: Sent: {self.bytes_sent_per_sec.value:.2f} B/s, "
                    f"Received: {self.bytes_recv_per_sec.value:.2f} B/s") 

class OmegaTradingCollector(PrometheusCollector):
    """Collector for OMEGA BTC AI trading metrics"""
    
    def __init__(self, registry: MetricsRegistry, trading_api_client=None):
        super().__init__(registry)
        self.collection_interval = 60
        self.trading_api_client = trading_api_client
        
        # Initialize metrics
        self.active_positions = GaugeMetric(
            "trading_active_positions",
            "Number of active trading positions",
            labels={"system": "omega_btc_ai"}
        )
        self.position_pnl = GaugeMetric(
            "trading_position_pnl",
            "Current PnL of all positions combined",
            labels={"system": "omega_btc_ai"}
        )
        self.trading_volume_24h = GaugeMetric(
            "trading_volume_24h",
            "Trading volume in the last 24 hours",
            labels={"system": "omega_btc_ai"}
        )
        self.order_success_rate = GaugeMetric(
            "trading_order_success_rate",
            "Percentage of successfully executed orders",
            labels={"system": "omega_btc_ai"}
        )
        self.trap_detection_confidence = GaugeMetric(
            "trading_trap_detection_confidence",
            "Current trap detection confidence level",
            labels={"system": "omega_btc_ai"}
        )
        
        # Register metrics
        self.registry.register_metric(self.active_positions)
        self.registry.register_metric(self.position_pnl)
        self.registry.register_metric(self.trading_volume_24h)
        self.registry.register_metric(self.order_success_rate)
        self.registry.register_metric(self.trap_detection_confidence)
    
    async def collect(self) -> None:
        """Collect trading metrics from the OMEGA BTC AI system"""
        # For now, use mock data if no client provided
        # In a real implementation, this would query your trading API
        if self.trading_api_client:
            # Real data collection would happen here
            positions = await self.trading_api_client.get_positions()
            pnl = await self.trading_api_client.get_total_pnl()
            volume = await self.trading_api_client.get_24h_volume()
            success_rate = await self.trading_api_client.get_order_success_rate()
            trap_confidence = await self.trading_api_client.get_trap_confidence()
        else:
            # Mock data for demonstration
            import random
            positions = random.randint(1, 10)
            pnl = random.uniform(-5.0, 15.0)
            volume = random.uniform(1000, 10000)
            success_rate = random.uniform(80, 99)
            trap_confidence = random.uniform(0, 100)
        
        # Update metrics
        self.active_positions.set(positions)
        self.position_pnl.set(pnl)
        self.trading_volume_24h.set(volume)
        self.order_success_rate.set(success_rate)
        self.trap_detection_confidence.set(trap_confidence)
        
        logger.debug(f"Collected trading metrics: Positions: {positions}, PnL: {pnl}, "
                    f"Trap Confidence: {trap_confidence}%")

class MatrixDisplay:
    """Terminal-based matrix display for the PROMETHEUS monitoring system"""
    
    def __init__(self, registry: MetricsRegistry):
        self.registry = registry
        self.running = False
        self.refresh_interval = 1.0  # seconds
        self.screen = None
        self.last_update = 0
        self.max_history = 60  # Store last 60 data points
        
        # Data history for graphing
        self.cpu_history = deque(maxlen=self.max_history)
        self.memory_history = deque(maxlen=self.max_history)
        self.net_recv_history = deque(maxlen=self.max_history)
        self.net_sent_history = deque(maxlen=self.max_history)
        self.trading_pnl_history = deque(maxlen=self.max_history)
        self.trap_confidence_history = deque(maxlen=self.max_history)
    
    def start(self):
        """Start the matrix display"""
        self.running = True
        curses.wrapper(self._run_display)
    
    def stop(self):
        """Stop the matrix display"""
        self.running = False
        if self.screen:
            curses.endwin()
    
    def _run_display(self, screen):
        """Main display loop"""
        self.screen = screen
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.use_default_colors()
        
        # Initialize color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Green on default
        curses.init_pair(2, curses.COLOR_RED, -1)    # Red on default
        curses.init_pair(3, curses.COLOR_YELLOW, -1) # Yellow on default
        curses.init_pair(4, curses.COLOR_BLUE, -1)   # Blue on default
        curses.init_pair(5, curses.COLOR_MAGENTA, -1) # Magenta on default
        curses.init_pair(6, curses.COLOR_CYAN, -1)   # Cyan on default
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE) # Title bar
        
        # Handle window resize
        screen.nodelay(1)  # Non-blocking input
        
        while self.running:
            try:
                # Check for keyboard input
                ch = screen.getch()
                if ch == ord('q'):
                    break
                
                # Update metrics history
                self._update_history()
                
                # Clear screen
                screen.clear()
                
                # Get terminal dimensions
                height, width = screen.getmaxyx()
                
                # Draw header
                self._draw_header(screen, width)
                
                # Draw system metrics panel
                self._draw_system_panel(screen, 3, 0, height // 2 - 3, width // 2)
                
                # Draw network metrics panel
                self._draw_network_panel(screen, 3, width // 2, height // 2 - 3, width // 2)
                
                # Draw trading metrics panel
                self._draw_trading_panel(screen, height // 2, 0, height // 2, width)
                
                # Draw graphs
                self._draw_graphs(screen, height // 2 + 2, width // 2 + 2, height // 2 - 4, width // 2 - 4)
                
                # Draw footer with help text
                self._draw_footer(screen, height - 1, width)
                
                # Refresh screen
                screen.refresh()
                
                # Sleep
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                # Log error but continue
                logger.error(f"Display error: {e}", exc_info=True)
                time.sleep(1)
    
    def _update_history(self):
        """Update metric history for graphs"""
        metrics = self.registry.get_all_metrics()
        
        # CPU usage
        cpu_metric = self.registry.get_metric("system_cpu_usage", {"host": socket.gethostname()})
        if cpu_metric:
            self.cpu_history.append(cpu_metric.value)
        
        # Memory usage
        memory_metric = self.registry.get_metric("system_memory_usage", {"host": socket.gethostname()})
        if memory_metric:
            self.memory_history.append(memory_metric.value)
        
        # Network metrics
        net_recv_metric = self.registry.get_metric("network_bytes_recv_per_sec", {"host": socket.gethostname()})
        if net_recv_metric:
            self.net_recv_history.append(net_recv_metric.value / 1024)  # KB/s
        
        net_sent_metric = self.registry.get_metric("network_bytes_sent_per_sec", {"host": socket.gethostname()})
        if net_sent_metric:
            self.net_sent_history.append(net_sent_metric.value / 1024)  # KB/s
        
        # Trading metrics
        pnl_metric = self.registry.get_metric("trading_position_pnl", {"system": "omega_btc_ai"})
        if pnl_metric:
            self.trading_pnl_history.append(pnl_metric.value)
        
        trap_metric = self.registry.get_metric("trading_trap_detection_confidence", {"system": "omega_btc_ai"})
        if trap_metric:
            self.trap_confidence_history.append(trap_metric.value)
    
    def _draw_header(self, screen, width):
        """Draw the header bar"""
        header = " OMEGA ^PROMETHEUS^ MATRIX Monitoring System "
        timestamp = datetime.datetime.now().strftime(" %Y-%m-%d %H:%M:%S ")
        padding = " " * (width - len(header) - len(timestamp) - 1)
        
        screen.attron(curses.color_pair(7) | curses.A_BOLD)
        screen.addstr(0, 0, header + padding + timestamp)
        screen.attroff(curses.color_pair(7) | curses.A_BOLD)
        
        # Subtitle
        screen.attron(curses.A_BOLD)
        screen.addstr(1, 1, "Foresight-driven system monitoring")
        screen.attroff(curses.A_BOLD)
    
    def _draw_system_panel(self, screen, y, x, height, width):
        """Draw system metrics panel"""
        # Panel border
        self._draw_box(screen, y, x, height, width, "System Metrics", curses.color_pair(4))
        
        # CPU usage
        cpu_metric = self.registry.get_metric("system_cpu_usage", {"host": socket.gethostname()})
        if cpu_metric:
            cpu_val = cpu_metric.value
            cpu_color = curses.color_pair(1) if cpu_val < 70 else curses.color_pair(3) if cpu_val < 90 else curses.color_pair(2)
            screen.addstr(y + 2, x + 2, f"CPU Usage: ")
            screen.attron(cpu_color)
            screen.addstr(f"{cpu_val:.1f}%")
            screen.attroff(cpu_color)
            self._draw_bar(screen, y + 3, x + 2, width - 4, cpu_val / 100, cpu_color)
        
        # Memory usage
        memory_metric = self.registry.get_metric("system_memory_usage", {"host": socket.gethostname()})
        memory_avail_metric = self.registry.get_metric("system_memory_available", {"host": socket.gethostname()})
        if memory_metric and memory_avail_metric:
            mem_val = memory_metric.value
            mem_color = curses.color_pair(1) if mem_val < 70 else curses.color_pair(3) if mem_val < 90 else curses.color_pair(2)
            avail_gb = memory_avail_metric.value / (1024 * 1024 * 1024)
            
            screen.addstr(y + 5, x + 2, f"Memory: ")
            screen.attron(mem_color)
            screen.addstr(f"{mem_val:.1f}%")
            screen.attroff(mem_color)
            screen.addstr(f" ({avail_gb:.1f} GB free)")
            self._draw_bar(screen, y + 6, x + 2, width - 4, mem_val / 100, mem_color)
        
        # Disk usage
        disk_metric = self.registry.get_metric("system_disk_usage", {"host": socket.gethostname(), "path": "/"})
        if disk_metric:
            disk_val = disk_metric.value
            disk_color = curses.color_pair(1) if disk_val < 70 else curses.color_pair(3) if disk_val < 90 else curses.color_pair(2)
            screen.addstr(y + 8, x + 2, f"Disk Usage: ")
            screen.attron(disk_color)
            screen.addstr(f"{disk_val:.1f}%")
            screen.attroff(disk_color)
            self._draw_bar(screen, y + 9, x + 2, width - 4, disk_val / 100, disk_color)
    
    def _draw_network_panel(self, screen, y, x, height, width):
        """Draw network metrics panel"""
        # Panel border
        self._draw_box(screen, y, x, height, width, "Network Metrics", curses.color_pair(6))
        
        # Network receive
        net_recv_metric = self.registry.get_metric("network_bytes_recv_per_sec", {"host": socket.gethostname()})
        if net_recv_metric:
            recv_val = net_recv_metric.value
            screen.addstr(y + 2, x + 2, f"Network Receive: ")
            screen.attron(curses.color_pair(6))
            # Format based on value size
            if recv_val < 1024:
                screen.addstr(f"{recv_val:.1f} B/s")
            elif recv_val < 1024 * 1024:
                screen.addstr(f"{recv_val/1024:.1f} KB/s")
            else:
                screen.addstr(f"{recv_val/(1024*1024):.2f} MB/s")
            screen.attroff(curses.color_pair(6))
        
        # Network send
        net_sent_metric = self.registry.get_metric("network_bytes_sent_per_sec", {"host": socket.gethostname()})
        if net_sent_metric:
            sent_val = net_sent_metric.value
            screen.addstr(y + 4, x + 2, f"Network Send: ")
            screen.attron(curses.color_pair(6))
            # Format based on value size
            if sent_val < 1024:
                screen.addstr(f"{sent_val:.1f} B/s")
            elif sent_val < 1024 * 1024:
                screen.addstr(f"{sent_val/1024:.1f} KB/s")
            else:
                screen.addstr(f"{sent_val/(1024*1024):.2f} MB/s")
            screen.attroff(curses.color_pair(6))
        
        # Total received
        bytes_recv_metric = self.registry.get_metric("network_bytes_recv", {"host": socket.gethostname()})
        if bytes_recv_metric:
            total_recv = bytes_recv_metric.value
            screen.addstr(y + 6, x + 2, f"Total Received: ")
            screen.attron(curses.color_pair(6))
            # Format based on value size
            if total_recv < 1024:
                screen.addstr(f"{total_recv:.1f} B")
            elif total_recv < 1024 * 1024:
                screen.addstr(f"{total_recv/1024:.1f} KB")
            elif total_recv < 1024 * 1024 * 1024:
                screen.addstr(f"{total_recv/(1024*1024):.2f} MB")
            else:
                screen.addstr(f"{total_recv/(1024*1024*1024):.2f} GB")
            screen.attroff(curses.color_pair(6))
        
        # Total sent
        bytes_sent_metric = self.registry.get_metric("network_bytes_sent", {"host": socket.gethostname()})
        if bytes_sent_metric:
            total_sent = bytes_sent_metric.value
            screen.addstr(y + 8, x + 2, f"Total Sent: ")
            screen.attron(curses.color_pair(6))
            # Format based on value size
            if total_sent < 1024:
                screen.addstr(f"{total_sent:.1f} B")
            elif total_sent < 1024 * 1024:
                screen.addstr(f"{total_sent/1024:.1f} KB")
            elif total_sent < 1024 * 1024 * 1024:
                screen.addstr(f"{total_sent/(1024*1024):.2f} MB")
            else:
                screen.addstr(f"{total_sent/(1024*1024*1024):.2f} GB")
            screen.attroff(curses.color_pair(6))
    
    def _draw_trading_panel(self, screen, y, x, height, width):
        """Draw trading metrics panel"""
        # Panel border
        self._draw_box(screen, y, x, height, width, "OMEGA BTC AI Trading Metrics", curses.color_pair(5))
        
        # Trading metrics - first column
        col1_x = x + 2
        
        # Active positions
        positions_metric = self.registry.get_metric("trading_active_positions", {"system": "omega_btc_ai"})
        if positions_metric:
            screen.addstr(y + 2, col1_x, f"Active Positions: ")
            screen.attron(curses.color_pair(5) | curses.A_BOLD)
            screen.addstr(f"{int(positions_metric.value)}")
            screen.attroff(curses.color_pair(5) | curses.A_BOLD)
        
        # PnL
        pnl_metric = self.registry.get_metric("trading_position_pnl", {"system": "omega_btc_ai"})
        if pnl_metric:
            pnl_val = pnl_metric.value
            pnl_color = curses.color_pair(1) if pnl_val >= 0 else curses.color_pair(2)
            screen.addstr(y + 4, col1_x, f"Position PnL: ")
            screen.attron(pnl_color | curses.A_BOLD)
            screen.addstr(f"{pnl_val:+.2f}%")
            screen.attroff(pnl_color | curses.A_BOLD)
        
        # Trading volume
        volume_metric = self.registry.get_metric("trading_volume_24h", {"system": "omega_btc_ai"})
        if volume_metric:
            screen.addstr(y + 6, col1_x, f"24h Volume: ")
            screen.attron(curses.color_pair(5))
            screen.addstr(f"${volume_metric.value:.2f}")
            screen.attroff(curses.color_pair(5))
        
        # Second column
        col2_x = x + width // 2 + 2
        
        # Order success rate
        success_metric = self.registry.get_metric("trading_order_success_rate", {"system": "omega_btc_ai"})
        if success_metric:
            success_val = success_metric.value
            success_color = curses.color_pair(1) if success_val >= 95 else curses.color_pair(3) if success_val >= 80 else curses.color_pair(2)
            screen.addstr(y + 2, col2_x, f"Order Success Rate: ")
            screen.attron(success_color)
            screen.addstr(f"{success_val:.1f}%")
            screen.attroff(success_color)
        
        # Trap detection confidence
        trap_metric = self.registry.get_metric("trading_trap_detection_confidence", {"system": "omega_btc_ai"})
        if trap_metric:
            trap_val = trap_metric.value
            trap_color = curses.color_pair(1) if trap_val >= 70 else curses.color_pair(3) if trap_val >= 30 else curses.color_pair(2)
            screen.addstr(y + 4, col2_x, f"Trap Detection Confidence: ")
            screen.attron(trap_color | curses.A_BOLD)
            screen.addstr(f"{trap_val:.1f}%")
            screen.attroff(trap_color | curses.A_BOLD)
            self._draw_bar(screen, y + 5, col2_x, width // 2 - 4, trap_val / 100, trap_color)
    
    def _draw_graphs(self, screen, y, x, height, width):
        """Draw performance graphs"""
        if len(self.cpu_history) > 1:
            # CPU graph
            self._draw_sparkline(screen, y, x, width, self.cpu_history, "CPU History (%)", curses.color_pair(4), 0, 100)
        
        if len(self.memory_history) > 1:
            # Memory graph
            self._draw_sparkline(screen, y + 6, x, width, self.memory_history, "Memory History (%)", curses.color_pair(3), 0, 100)
        
        if len(self.trading_pnl_history) > 1:
            # PnL graph (can go negative)
            min_pnl = min(min(self.trading_pnl_history), -5)  # At least -5
            max_pnl = max(max(self.trading_pnl_history), 5)   # At least +5
            self._draw_sparkline(screen, y + 12, x, width, self.trading_pnl_history, "PnL History (%)", curses.color_pair(5), min_pnl, max_pnl)
    
    def _draw_footer(self, screen, y, width):
        """Draw footer with help text"""
        footer = " Press 'q' to quit | LINUX TERMINAL TORVALDS OMEGA GNU 3.0 STYLE "
        screen.attron(curses.color_pair(7))
        screen.addstr(y, 0, footer + " " * (width - len(footer) - 1))
        screen.attroff(curses.color_pair(7))
    
    def _draw_box(self, screen, y, x, height, width, title=None, color=0):
        """Draw a box with optional title"""
        # Top and bottom borders
        screen.attron(color)
        screen.addstr(y, x, "┌" + "─" * (width - 2) + "┐")
        screen.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘")
        
        # Side borders
        for i in range(1, height - 1):
            screen.addstr(y + i, x, "│")
            screen.addstr(y + i, x + width - 1, "│")
        
        # Title if provided
        if title:
            title = f" {title} "
            if len(title) < width - 4:
                screen.addstr(y, x + 2, title)
        
        screen.attroff(color)
    
    def _draw_bar(self, screen, y, x, width, percentage, color=0):
        """Draw a progress bar"""
        filled_width = int(width * percentage)
        screen.attron(color)
        screen.addstr(y, x, "[" + "=" * filled_width + " " * (width - filled_width - 2) + "]")
        screen.attroff(color)
    
    def _draw_sparkline(self, screen, y, x, width, data, title=None, color=0, min_val=None, max_val=None):
        """Draw a sparkline graph"""
        if not data:
            return
        
        # Draw title
        if title:
            screen.attron(color | curses.A_BOLD)
            screen.addstr(y, x, title)
            screen.attroff(color | curses.A_BOLD)
            y += 1
        
        # Determine min/max values if not provided
        if min_val is None:
            min_val = min(data)
        if max_val is None:
            max_val = max(data)
        
        # Ensure min and max are different
        if min_val == max_val:
            if min_val == 0:
                max_val = 1
            else:
                min_val = 0.9 * min_val
                max_val = 1.1 * max_val
        
        # Height of graph (4 lines)
        graph_height = 4
        
        # Draw y-axis labels
        screen.addstr(y, x - 5, f"{max_val:5.1f}")
        screen.addstr(y + graph_height - 1, x - 5, f"{min_val:5.1f}")
        
        # Draw graph box
        self._draw_box(screen, y, x, graph_height + 2, width, None, color)
        
        # Draw data points
        points_to_draw = min(len(data), width - 4)
        data_slice = list(data)[-points_to_draw:]
        
        for i, val in enumerate(data_slice):
            # Scale to graph height
            scaled_val = (val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
            point_height = int(scaled_val * (graph_height - 1))
            
            # Plot point
            point_char = "▓"
            screen.attron(color)
            screen.addstr(y + graph_height - 1 - point_height, x + 2 + i, point_char)
            screen.attroff(color) 

class PrometheusMatrix:
    """Main class for the OMEGA PROMETHEUS MATRIX monitoring system"""
    
    def __init__(self):
        self.registry = MetricsRegistry()
        self.collectors = []
        self.display = None
        self.running = False
        self.event_loop = None
    
    def add_collector(self, collector):
        """Add a collector to the monitoring system"""
        self.collectors.append(collector)
    
    async def start_collectors(self):
        """Start all collectors in the background"""
        tasks = []
        for collector in self.collectors:
            tasks.append(asyncio.create_task(collector.run()))
        return tasks
    
    def start_display(self):
        """Start the matrix display in a separate thread"""
        import threading
        self.display = MatrixDisplay(self.registry)
        display_thread = threading.Thread(target=self.display.start)
        display_thread.daemon = True
        display_thread.start()
        return display_thread
    
    async def run(self):
        """Run the PROMETHEUS MATRIX monitoring system"""
        self.running = True
        
        # Setup signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.event_loop.add_signal_handler(
                sig, lambda s=sig: asyncio.create_task(self.shutdown(s))
            )
        
        # Start collectors
        collector_tasks = await self.start_collectors()
        
        # Start display
        display_thread = self.start_display()
        
        # Wait until shutdown
        while self.running:
            await asyncio.sleep(1)
        
        # Cancel collector tasks on shutdown
        for task in collector_tasks:
            task.cancel()
        
        # Wait for tasks to be cancelled
        await asyncio.gather(*collector_tasks, return_exceptions=True)
        
        # Stop display
        if self.display:
            self.display.stop()
            
        # Wait for display thread to end
        if display_thread.is_alive():
            display_thread.join(timeout=5)
    
    async def shutdown(self, signal=None):
        """Gracefully shutdown the monitoring system"""
        if signal:
            logger.info(f"Received exit signal {signal.name}...")
        
        logger.info("Shutting down PROMETHEUS MATRIX monitoring system...")
        self.running = False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="OMEGA PROMETHEUS MATRIX Monitoring System")
    
    parser.add_argument("--collect-system", action="store_true", 
                         help="Collect system metrics (CPU, memory, disk)")
    parser.add_argument("--collect-network", action="store_true",
                         help="Collect network metrics")
    parser.add_argument("--collect-trading", action="store_true", 
                         help="Collect trading metrics from OMEGA BTC AI")
    parser.add_argument("--all", action="store_true",
                         help="Enable all collectors")
    parser.add_argument("--no-display", action="store_true",
                         help="Run without the matrix display (headless mode)")
    parser.add_argument("--interval", type=int, default=60,
                         help="Default collection interval in seconds")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                         default="INFO", help="Set logging level")
    
    return parser.parse_args()

def setup_logging(log_level):
    """Configure logging based on command line arguments"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    logging.getLogger().setLevel(numeric_level)
    
    # Add a console handler for when running without display
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logging.getLogger().addHandler(console_handler)

async def main():
    """Main entry point for the OMEGA PROMETHEUS MATRIX monitoring system"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Print banner
    print_banner()
    
    # Create the PROMETHEUS MATRIX system
    prometheus = PrometheusMatrix()
    prometheus.event_loop = asyncio.get_event_loop()
    
    # Add collectors based on arguments
    if args.collect_system or args.all:
        logger.info("Enabling system metrics collector")
        prometheus.add_collector(SystemCollector(prometheus.registry))
    
    if args.collect_network or args.all:
        logger.info("Enabling network metrics collector")
        prometheus.add_collector(NetworkCollector(prometheus.registry))
    
    if args.collect_trading or args.all:
        logger.info("Enabling OMEGA BTC AI trading metrics collector")
        prometheus.add_collector(OmegaTradingCollector(prometheus.registry))
    
    # If no collectors were specified, enable all
    if not prometheus.collectors:
        logger.info("No collectors specified, enabling all collectors")
        prometheus.add_collector(SystemCollector(prometheus.registry))
        prometheus.add_collector(NetworkCollector(prometheus.registry))
        prometheus.add_collector(OmegaTradingCollector(prometheus.registry))
    
    # Set collection intervals
    for collector in prometheus.collectors:
        collector.collection_interval = args.interval
    
    # Run the PROMETHEUS MATRIX system
    if args.no_display:
        logger.info("Running in headless mode (no display)")
        # Just start collectors without display
        collector_tasks = await prometheus.start_collectors()
        
        # Run until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        finally:
            # Cancel collector tasks
            for task in collector_tasks:
                task.cancel()
            
            # Wait for tasks to be cancelled
            await asyncio.gather(*collector_tasks, return_exceptions=True)
    else:
        # Run with display
        await prometheus.run()

def print_banner():
    """Print ASCII art banner"""
    banner = r"""
   ____  __  ___ ______ ____   ___      ____  ____   ____  __  ___ ______ ______  __  ___ ______ __  __ _____ 
  / __ \/  |/  // ____// __ \ /   |    / __ \/ __ \ / __ \/  |/  // ____//_  __/ /  |/  // ____// / / // ___/
 / / / / /|_/ // __/  / /_/ // /| |   / /_/ / /_/ // /_/ / /|_/ // __/    / /   / /|_/ // __/  / / / / \__ \ 
/ /_/ / /  / // /___ / _, _// ___ |  / ____/ _, _// _, _/ /  / // /___   / /   / /  / // /___ / /_/ / ___/ / 
\____/_/  /_//_____//_/ |_|/_/  |_| /_/   /_/ |_|/_/ |_/_/  /_//_____/  /_/   /_/  /_//_____/ \____/ /____/  
                                                                                                               
 __  ___ ___   ______  ____ __ __ __
/  |/  //   | /_  __/ / __ \\ \/ // /
/ /|_/ // /| |  / /   / /_/ / \  // / 
/ /  / // ___ | / /   / _, _/  / //_/  
/_/  /_//_/  |_|/_/   /_/ |_|  /_/(_)   
                                       
LINUX TERMINAL TORVALDS OMEGA GNU 3.0 STYLE
"""
    print(banner)
    print("\nForesight-driven system monitoring\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting OMEGA PROMETHEUS MATRIX monitoring system...")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1) 