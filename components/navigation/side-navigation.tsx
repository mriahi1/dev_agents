'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslation } from 'react-i18next';
import { NAV_KEYS } from '@/lib/constants/translation-keys';

// ... existing imports ...

export function SideNavigation() {
  const { t } = useTranslation(['common', 'navigation']);
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const navigationItems = [
    {
      href: '/dashboard',
      label: t(NAV_KEYS.DASHBOARD),
      icon: DashboardIcon,
    },
    {
      href: '/properties',
      label: t(NAV_KEYS.PROPERTIES),
      icon: PropertiesIcon,
    },
    {
      href: '/tenants',
      label: t(NAV_KEYS.TENANTS),
      icon: TenantsIcon,
    },
    {
      href: '/leases',
      label: t(NAV_KEYS.LEASES),
      icon: LeasesIcon,
    },
    {
      href: '/settings',
      label: t(NAV_KEYS.SETTINGS),
      icon: SettingsIcon,
    },
  ];

  return (
    <nav className="side-navigation">
      {navigationItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`nav-item ${pathname === item.href ? 'active' : ''}`}
        >
          <item.icon />
          {!isCollapsed && <span>{item.label}</span>}
        </Link>
      ))}
    </nav>
  );
} 