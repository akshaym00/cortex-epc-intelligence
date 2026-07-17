import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DashboardCard from './DashboardCard';

const entityItem = {
  id: 'entity-123',
  name: 'Generator Delivery',
  entity_type: 'equipment',
  description: 'Delivery of generator',
};

const relationshipItem = {
  source: 'Generator Delivery',
  source_entity_id: 'entity-123',
  relationship_type: 'supplies',
  target: 'Site Installation',
  target_entity_id: 'entity-456',
};

describe('DashboardCard', () => {
  it('calls onEntityClick when an entity name is clicked', () => {
    const handleEntityClick = vi.fn();

    render(
      <DashboardCard
        id="entities"
        title="Project Entities"
        items={[entityItem]}
        onEntityClick={handleEntityClick}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /Generator Delivery/i }));

    expect(handleEntityClick).toHaveBeenCalledWith('entity-123');
  });

  it('calls onEntityClick when relationship source or target names are clicked', () => {
    const handleEntityClick = vi.fn();

    render(
      <DashboardCard
        id="relationships"
        title="Dependency Network"
        items={[relationshipItem]}
        onEntityClick={handleEntityClick}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /Generator Delivery/i }));
    fireEvent.click(screen.getByRole('button', { name: /Site Installation/i }));

    expect(handleEntityClick).toHaveBeenCalledTimes(2);
    expect(handleEntityClick).toHaveBeenCalledWith('entity-123');
    expect(handleEntityClick).toHaveBeenCalledWith('entity-456');
  });
});
